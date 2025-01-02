import torch
from botorch.utils.multi_objective import is_non_dominated
from botorch.utils.multi_objective import infer_reference_point

tkwargs = {
    "dtype": torch.double,
    "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
}

def find_ref_point(observed_value:torch.Tensor):
    # 调用is_non_dominated函数
    pareto_mask = is_non_dominated(observed_value)
    # 使用mask来获取Pareto最优点
    pareto_points = observed_value[pareto_mask]
    # 我们可以直接调用函数来推断参考点
    reference_point = infer_reference_point(pareto_points)
    return reference_point