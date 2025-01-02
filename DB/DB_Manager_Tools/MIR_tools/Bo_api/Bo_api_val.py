from pydantic import BaseModel, conint, constr, ValidationError
from fastapi import FastAPI, BackgroundTasks, Body, UploadFile, File,Form
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Depends, HTTPException
import json
from pydantic import Field
import pandas as pd
from io import BytesIO
# 参数验证
class TaskParams(BaseModel):
    opt_direction: constr(regex='^(max|min)$') = "max"
    opt_dim: conint(ge=1) = 1
    acq_function: constr(regex='^(EI|UCB|PI|qNEHVI|qEHVI)$') = "EI"

# 定义依赖项函数用于处理 TaskParams
def get_task_params(
        opt_direction: str = Form(default="max", description="Optimization direction, max or min."),
        opt_dim: int = Form(default=1, description="Single-objective optimization is 1 and multi-objective optimization is a positive integer greater than 1."),
        acq_function: str = Form(default="EI",description="One of EI,UCB,PI is selected for single objective optimization and one of qNEHVI,qEHVI is selected for multi-objective optimization.")
):
    try:
        return TaskParams(opt_direction=opt_direction, opt_dim=opt_dim, acq_function=acq_function)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

async def read_file(file):
    if file.content_type == "text/csv":
        return pd.read_csv(BytesIO(await file.read()))
    elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return pd.read_excel(BytesIO(await file.read()))
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

async def vaild_train_can(train_data,candidate_space,task_params):
    try:
        feature_list = list(train_data.columns)[:-task_params.opt_dim]
        candidate_space.columns = feature_list

        # 去除重复行
        # 首先，找出两个 DataFrame 中共有的行
        common_rows = pd.merge(candidate_space, train_data[feature_list], how='inner')
        print("common_rows:",common_rows)
        # 然后，从 df1 中删除这些行
        candidate_space = candidate_space[~candidate_space.isin(common_rows)].dropna(how='all')
        # 返回合并后的DataFrame
        return candidate_space
    except ValueError as e:
        # 如果发生错误，返回400状态码和错误信息
        raise HTTPException(status_code=400, detail="训练集和候选空间格式不匹配。")

async def vaild_params(params):
    if params["opt_dim"] ==1:
        if params["acq_function"] not in ["EI","UCB","PI"]:
            raise HTTPException(status_code=400, detail="单目标优化获取函数只能使用EI,UCB,PI")
    elif params["opt_dim"] !=1:
        if params["acq_function"] not in ["qEHVI", "qNEHVI"]:
            raise HTTPException(status_code=400, detail="多目标优化获取函数只能使用qEHVI,qNEHVI")