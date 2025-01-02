import numpy as np
from itertools import product
import pandas as pd



class DataPreprocessor:
    def __init__(self, data, params=None):
        self.metadata = {}
        if params:
            for key, value in params.items():
                setattr(self, key, value)
        else:
            self.mean = np.mean(data, axis=0)
            self.std = np.std(data, axis=0)
            self.max = np.max(data, axis=0)
            self.min = np.min(data, axis=0)
            metadata = {}
            self.params = {"mean": self.mean, "std": self.std, "max": self.max, "min": self.min}

    def normalize(self, data, dim):

        start, end = dim
        # 执行归一化处理
        normalized_data = (data - self.min[start:end]) / (self.max[start:end] - self.min[start:end])
        self.normalized = True
        return normalized_data

    def unnormalize(self, data, dim):
        start, end = dim
        # 执行反归一化处理
        unnormalized_data = data * (self.max[start:end] - self.min[start:end]) + self.min[start:end]
        self.normalized = False
        return unnormalized_data

    def scale(self, data, dim):
        # 执行标准化处理
        start, end = dim
        scaled_data = (data - self.mean[start:end]) / self.std[start:end]
        self.scaled = True
        return scaled_data

    def unscale(self, data, dim):
        # 执行反标准化处理
        start, end = dim
        unscaled_data = data * self.std[start:end] + self.mean[start:end]
        self.scaled = False
        return unscaled_data

def generate_candidate_space(dictionary):
    # 提取每个嵌套字典的范围
    ranges = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            ranges.append(generate_candidate_space(value))  # 递归处理嵌套字典
        else:
            start, stop, step = value
            ranges.append(np.arange(start, stop, step))
#     print(ranges)
    # 生成所有组合的笛卡尔积
    grid = list(product(*ranges))
    # 转换为 np.array
    candidate_space = pd.DataFrame(np.array(grid))
    return candidate_space