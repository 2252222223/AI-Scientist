import torch
from botorch.acquisition import ExpectedImprovement, ProbabilityOfImprovement, UpperConfidenceBound
from botorch.acquisition.multi_objective.monte_carlo import (
    qExpectedHypervolumeImprovement,
    qNoisyExpectedHypervolumeImprovement,
)
from botorch.utils.multi_objective.box_decompositions.non_dominated import (
    FastNondominatedPartitioning,
)
from botorch.sampling.normal import SobolQMCNormalSampler
from typing import Optional
import numpy as np
from DB.DB_Manager_Tools.MIR_tools.Bo_api.Base import tkwargs


def acq_fuction(model:torch.nn.Module,params:dict,best_observed_value:Optional[torch.Tensor]=None,train_x_pred:Optional[torch.Tensor]=None,ref_point:Optional[torch.Tensor]=None,train_data:Optional[np.ndarray]=None):
    if params["acq_function"]=="EI":
        acq_fun = ExpectedImprovement(model=model, best_f=best_observed_value,maximize=True)
    elif params["acq_function"]=="UCB":
        acq_fun = UpperConfidenceBound(model=model, beta=0.1,maximize=True) #beta越高越倾向于探索
    elif params["acq_function"]=="PI":
        acq_fun = ProbabilityOfImprovement(model=model, best_f=best_observed_value,maximize=True)
    elif params["acq_function"]=="qEHVI":

        # 对超体积进行划分，返回是布尔类型
        partitioning = FastNondominatedPartitioning(ref_point=ref_point, Y=train_x_pred)
        # 定义获取函数
        # 不管如何，将前边的划分赋给采集函数
        acq_fun = qExpectedHypervolumeImprovement(
            model = model,
            ref_point = ref_point,
            partitioning = partitioning
        )
    elif params["acq_function"]=="qNEHVI":
        # define the qEI and qNEI acquisition modules using a QMC sampler
        qnehvi_sampler = SobolQMCNormalSampler(sample_shape=torch.Size([1]))
        acq_fun = qNoisyExpectedHypervolumeImprovement(
            model=model,
            ref_point=ref_point.tolist(),  # use known reference point
            X_baseline=torch.tensor(train_data[:,:-params["opt_dim"]],**tkwargs),
            prune_baseline=True,  # prune baseline points that have estimated zero probability of being Pareto optimal
            sampler=qnehvi_sampler,
        )
    return acq_fun
