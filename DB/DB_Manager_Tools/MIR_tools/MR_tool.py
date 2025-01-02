import os
#环境变量要设置到最前面，加载包的前面，不然无法传进去
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
import pandas as pd
from DB.DB_Manager_Tools.MIR_tools.Bo_api.GP_tool import active_learning
from DB.DB_Manager_Tools.MIR_tools.Bo_api.knowledge_based_reasoning import get_initial_value, get_next_unkonw_value, GPT4_res, history_save, LLM_decison_save, Response_format
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=40)
#环境变量要设置到最前面，加载包的前面，不然无法传进去
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type

def BO_filter(params):
    train_data_path = params["train_data_path"]
    candidate_space_path = params["candidate_space_path"]
    train_data = pd.read_excel(train_data_path)
    candidate_space = pd.read_excel(candidate_space_path)
    input_params = {"know_point": train_data, "candidate_space": candidate_space,
                    "opt_direction": params["opt_direction"], "opt_dim": params["opt_dim"],
                    "acq_function": params["acq_function"], "feature_nums": len(train_data.columns)}
    new_x, candidate_data_pred, lower_bound, upper_bound, acq_value, sorted_indices = active_learning(input_params)
    columns_name = train_data.columns
    new_x_rank = pd.DataFrame(new_x, columns=columns_name[:-input_params["opt_dim"]])

    return new_x_rank

def knowledge_recommend(params,new_x_rank):
    aa = get_initial_value(params["train_data_path"])
    bb = get_next_unkonw_value(new_x_rank)
    file_name = 'GPT4-decision.txt'
    # 检查文件是否存在
    if os.path.isfile(file_name):
        with open('example.txt', 'r', encoding='utf-8') as file:
            history = file.read()
        print("不存在")
    else:
        history = ""
    kk = GPT4_res({"Response_format":Response_format,"initial_value": aa, "history": history, "Unknown_space":bb})
    history = history_save(history, "MatterAI", kk["text"])
    # print(kk["text"])
    LLM_decison_save(kk["text"])
    return kk["text"]



class MR_PreSchema(BaseModel):
    train_data_path: str = Field(description="Should be a known space or training dataset address.")
    candidate_space_path: str = Field(description = "Should be a candidate space dataset address.")
    opt_direction: str =Field(description = "Should be the optimization direction, only max or min can be entered.")
    opt_dim: int = Field(description = "Should be an optimization dimension, as a positive integer.")

class MR_Reasoning(BaseTool):
    name = "Material reasoning"
    description = "Useful when combining data and knowledge reasoning to optimize material performance."
    args_schema: Type[BaseModel] = MR_PreSchema

    def _run(self, train_data_path: str, candidate_space_path: str, opt_direction: str, opt_dim: int) -> str:
        params = {"train_data_path": train_data_path, "candidate_space_path": candidate_space_path,
                  "opt_direction": opt_direction, "opt_dim": int(opt_dim)}
        if params["opt_dim"] ==1:
            params["acq_function"] ="EI"
        else:
            params["acq_function"] ="qEHVI"

        new_x_rank = BO_filter(params)
        LLM_recommend = knowledge_recommend(params, new_x_rank)
        return LLM_recommend

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")
