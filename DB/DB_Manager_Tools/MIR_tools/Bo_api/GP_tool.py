import torch
import numpy as np
from botorch.models import SingleTaskGP
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.models.transforms.outcome import Standardize
from botorch import fit_gpytorch_mll
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from gpytorch.mlls import ExactMarginalLogLikelihood
from DB.DB_Manager_Tools.MIR_tools.Bo_api.Base import tkwargs,find_ref_point
from DB.DB_Manager_Tools.MIR_tools.Bo_api.DataProcessing import DataPreprocessor
from DB.DB_Manager_Tools.MIR_tools.Bo_api.AcquctionFunction import acq_fuction


def initialize_model(train_data,opt_dim,params):
    # define models for objective and constraint
    train_data = torch.tensor(train_data,**tkwargs)
    models = []
    train_X = train_data[:,:train_data.shape[-1] - opt_dim]
    train_Y = train_data[:,train_data.shape[-1] - opt_dim:]
    if params["opt_dim"]==1:
        model = SingleTaskGP(train_X, train_Y, outcome_transform=Standardize(m=1))
        mll = ExactMarginalLogLikelihood(model.likelihood, model)
        best_observed_value = train_Y.max()
        return mll, model,best_observed_value
    else:
        for i in range(train_Y.shape[-1]):
            train_y = train_Y[..., i: i + 1]
            models.append(
                SingleTaskGP(
                    train_X, train_y, outcome_transform=Standardize(m=1)
                )
            )
        model = ModelListGP(*models)
        mll = SumMarginalLogLikelihood(model.likelihood, model)
        reference_point = find_ref_point(torch.tensor(np.array(params["know_point"])[:,-opt_dim:]))
        return mll, model,reference_point

def get_next_point(acq_fun,params,candidate_space_processor,candidate_data):

    acq_value = []
    for i in range(len(candidate_data)):
        acq_value.append(acq_fun(torch.tensor(candidate_data[i],**tkwargs).unsqueeze(0)).detach().cpu().numpy())
    # 从大到小排序并获取索引
#     print(acq_value)
    acq_value = np.array(acq_value).squeeze()
    sorted_indices = np.argsort(-acq_value)
    x_next = candidate_data[sorted_indices]
    # observe new values
    new_x = candidate_space_processor.unnormalize(x_next,dim=(0,-params["opt_dim"]))
    return new_x,acq_value[sorted_indices],sorted_indices

def active_learning(params):

    if params["opt_direction"] == "min":
        train_data = params["know_point"]
        train_data[list(train_data.columns)[-params["opt_dim"]:]] = train_data[list(train_data.columns)[-params["opt_dim"]:]] * -1
        params["know_point"] = train_data

    train_data_processor = DataPreprocessor(np.array(params["know_point"]))
    candidate_space_processor = DataPreprocessor(np.array(params["candidate_space"]), train_data_processor.params)

    train_data_nor = train_data_processor.normalize(np.array(params["know_point"]), dim=(0, params["feature_nums"]))

    candidate_data = candidate_space_processor.normalize(np.array(params["candidate_space"]),dim=(0, -params["opt_dim"]))
    # 模型初始化
    mll, model, best_observed_value = initialize_model(train_data=train_data_nor, opt_dim=params["opt_dim"], params=params)
    # 训练模型
    fit_gpytorch_mll(mll)
    # 得到训练集预测值
    with torch.no_grad():
        train_x_pred = model.posterior(torch.tensor(train_data_nor[:, :-params["opt_dim"]], **tkwargs)).mean
        test_x_nor = candidate_space_processor.normalize(np.array(params["candidate_space"]),dim=(0,-params["opt_dim"]))


    # 采集函数
    if params["opt_dim"] == 1:
        acq_fun = acq_fuction(model=model, params=params, best_observed_value=best_observed_value)
    else:
        acq_fun = acq_fuction(model=model, params=params, train_x_pred=train_x_pred,
                              ref_point=best_observed_value.to(tkwargs["device"]), train_data=train_data_nor)
    # 获取下一个点
    new_x, acq_value, sorted_indices = get_next_point(acq_fun=acq_fun, params=params, candidate_space_processor=candidate_space_processor,candidate_data =candidate_data)

    with torch.no_grad():
        candidate_data_preds = model.posterior(torch.tensor(candidate_data, **tkwargs))
        pred_cand_y = candidate_space_processor.unnormalize(candidate_data_preds.mean.detach().cpu().numpy(),dim=(params["feature_nums"]-params["opt_dim"], params["feature_nums"]))
        pred_cand_y = pred_cand_y[sorted_indices]

        mean= pred_cand_y
        std_dev= candidate_data_preds.variance.sqrt().detach().cpu().numpy()
        std_dev = std_dev[sorted_indices]
        lower_bound = mean - 1.96 * std_dev
        upper_bound = mean + 1.96 * std_dev
    if params["opt_direction"] == "min":
        pred_cand_y = pred_cand_y * -1
    return new_x, pred_cand_y, lower_bound, upper_bound, acq_value, sorted_indices


