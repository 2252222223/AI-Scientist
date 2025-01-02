from GP_tool import active_learning
import torch
import pandas as pd
from Base import tkwargs,find_ref_point
from botorch.test_functions.multi_objective import BraninCurrin
from botorch.utils.sampling import draw_sobol_samples
problem = BraninCurrin(negate=True).to(**tkwargs)
from botorch.utils.multi_objective.box_decompositions.dominated import (
    DominatedPartitioning,
)

def gen_cand():
    x = draw_sobol_samples(bounds=problem.bounds, n=3000, q=1).squeeze(1)
    y = problem(x)
    return pd.DataFrame(x.cpu().numpy())

#多目标优化
train_x = draw_sobol_samples(bounds=problem.bounds, n=20, q=1).squeeze(1)
train_y = problem(train_x)
ref_point = find_ref_point(train_y)

# #定义f(x)
# def real_function(x):
#     return np.exp(-0.2*(x-2)**2) + 1.5*np.exp(-0.2*(x-15)**2) + 0.8*np.exp(-0.2*(x-10)**2)
#
# x_real = np.linspace(0, 20, 1000)
# y_real = real_function(x_real)
#
# # 初始点
# x_sampled_points = np.random.choice(x_real, size=3, replace=False)
hvs_list = []
# compute hypervolume
bd = DominatedPartitioning(ref_point=ref_point, Y=problem(train_x))
volume = bd.compute_hypervolume().item()
hvs_list.append(volume)


for n in range(10):
    # if "next_x" in dir():
    #     x_sampled_points = np.append(x_sampled_points, next_x)
    # y_sampled_points = real_function(x_sampled_points)
    # print(y_sampled_points.max())
    # train_data = pd.DataFrame()
    # train_data["X"] = x_sampled_points
    # train_data["Y"] = y_sampled_points
    # candidate_space = generate_candidate_space({'var1': (0, 20, 0.01)})
    if "next_x" in dir():
        if len(next_x.shape)==1:
            train_x = torch.cat((train_x, torch.tensor(next_x,**tkwargs).unsqueeze(0)),dim=0)
        else:
            train_x = torch.cat((train_x, torch.tensor(next_x,**tkwargs)),dim=0)
    train_y = problem(train_x)
    train_data = pd.DataFrame(torch.cat((train_x, train_y), dim=1).cpu().numpy())
    candidate_space = gen_cand()

    params = {"know_point": train_data, "candidate_space": candidate_space, "opt_direction": "max", "opt_dim": 2,
              "acq_function": "qNEHVI", "feature_nums": len(train_data.columns)}



    new_x, candidate_data_pred, lower_bound, upper_bound, acq_value, sorted_indices = active_learning(params)
    # next_x = new_x[0]
    # next_y = real_function(next_x)

    # print(new_x, candidate_data_pred, acq_value, sorted_indices)
    # print(next_x, next_y, candidate_data_pred[0])
    # 下一个点
    next_x = new_x[0:10]
    next_y = problem(torch.tensor(next_x, **tkwargs))
    if len(next_y.shape) == 1:
        next_y = next_y.unsqueeze(0)

    # compute hypervolume
    bd = DominatedPartitioning(ref_point=problem.ref_point.cpu(), Y=torch.cat([train_y, next_y]).cpu())
    volume = bd.compute_hypervolume().item()
    hvs_list.append(volume)

print(hvs_list)
print(lower_bound)