import os
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
from langchain.tools import BaseTool
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.Submit_task import submit_experiment_task, create_auto_lab_task_data
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.Devices import (get_XRD_all_parameters,get_WLDWT_all_parameters,
                                                             get_GTLPF_all_parameters,get_QMGYW_all_parameters,
                                                             get_SGKGJ_all_parameters,get_QMGQMJ_all_parameters,
                                                             get_RQZH_all_parameters, get_TCYPJ_all_parameters,
                                                             get_GTLHCGW_all_parameters,get_GSL_all_parameters,
                                                             get_ESPSJ_all_parameters)
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.base import get_current_time, modify_experimental_parameters, task_parse_prompt, get_drug_setting
from pydantic import BaseModel, Field, conint
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from typing import Optional, Type
import json
state = {"Tank1":"Li2CO3", "Tank2": "LIF", "Tank3": "MnO", "Tank4": "TiO2","Tank5":"Mn2O3"}

def modify_GTLPF(device_configs,device_nodedatas,Parameters):

    GTLPF_all_parameters_1 = get_GTLPF_all_parameters()
    # 药品罐的位置状态
    state = get_drug_setting()
    # 初始的设备参数
    GTLPF_modify_parameters_1 = {
        "materialCup1_Status": True
    }
    # 创建一个映射表，将药品名称与对应的重量匹配
    drug_weight_map = {drug['drug_name']: drug['mass'] for drug in Parameters}
    # 根据需求更新设备参数
    for tank, drug_name in state.items():
        # 找到药品对应的重量
        if drug_name in drug_weight_map:
            weight = drug_weight_map[drug_name]
            # 更新对应的罐子
            GTLPF_modify_parameters_1[f"materialCup1_{tank}_Weight"] = int(weight)
            GTLPF_modify_parameters_1[f"materialCup1_{tank}_Status"] = True
        else:
            # 如果该药品不存在于列表中，设置罐子为未启用
            GTLPF_modify_parameters_1[f"materialCup1_{tank}_Status"] = False
            GTLPF_modify_parameters_1[f"materialCup1_{tank}_Weight"] = 0
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GTLPF_all_parameters_1, GTLPF_modify_parameters_1)
    return device_configs,device_nodedatas

def modify_QMGQMJ(device_configs,device_nodedatas,Parameters):
    QMGQMJ_all_parameters_1 = get_QMGQMJ_all_parameters()
    QMGQMJ_runing_time = Parameters["runing_time"]
    QMGQMJ_runing_speed = Parameters["runing_spend"]
    QMGQMJ_modify_parameters_1 = {}
    QMGQMJ_modify_parameters_1["loopNumber"] = min(int(QMGQMJ_runing_time/360), 15)
    QMGQMJ_modify_parameters_1["speed_1"] = QMGQMJ_runing_speed
    QMGQMJ_modify_parameters_1["speed_2"] = QMGQMJ_runing_speed
    QMGQMJ_modify_parameters_1["speed_3"] = QMGQMJ_runing_speed
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      QMGQMJ_all_parameters_1, QMGQMJ_modify_parameters_1)
    return device_configs, device_nodedatas

def modify_TCYPJ(device_configs,device_nodedatas,Parameters):
    TCYPJ_all_parameters_1 = get_TCYPJ_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      TCYPJ_all_parameters_1)
    return device_configs, device_nodedatas


def modify_GSL(device_configs,device_nodedatas,Parameters):
    Temperature_set = Parameters
    Temperature_modify_parameters = []
    for i in Temperature_set:
        single_stage = {}
        single_stage["key"] = ""
        if i["time"] == None or i["time"] == "None":
            single_stage["time"] = (i["target_temperature"] - i["start_temperature"])/10
        else:
            single_stage["time"] = i["time"]
        single_stage["temperature"] = i["target_temperature"]
        single_stage["speed"] = 0
        Temperature_modify_parameters.append(single_stage)

    GSL_all_parameters = get_GSL_all_parameters()
    GSL_modify_parameters_1 ={}
    GSL_modify_parameters_1["param"] = Temperature_modify_parameters
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GSL_all_parameters, GSL_modify_parameters_1)
    return device_configs, device_nodedatas


def modify_ESPSJ(device_configs, device_nodedatas,Parameters):
    ESPSJ_all_parameters = get_ESPSJ_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      ESPSJ_all_parameters)
    return device_configs, device_nodedatas

def modify_XRD(device_configs, device_nodedatas,Parameters):
    #XRD
    XRD_modify_parameters_1 = Parameters
    XRD_all_parameters = get_XRD_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      XRD_all_parameters,XRD_modify_parameters_1)
    return device_configs, device_nodedatas


def universal_task_submit(process_parameter):
    device_configs = []
    device_nodedatas = []
    for step in process_parameter:
        if step["Equipment"] != "None":
            if step["Equipment"] == "Powder Loading Systems":
                device_configs, device_nodedatas = modify_GTLPF(device_configs, device_nodedatas, step["Parameters"])
            elif step["Equipment"] =="Ball Mill":
                device_configs, device_nodedatas = modify_QMGQMJ(device_configs, device_nodedatas, step["Parameters"])
            elif step["Equipment"] =="Tablet Press":
                device_configs, device_nodedatas = modify_TCYPJ(device_configs,device_nodedatas,step["Parameters"])
            elif step["Equipment"] == "Tube Furnace":
                device_configs, device_nodedatas = modify_GSL(device_configs,device_nodedatas,step["Parameters"])
            elif step["Equipment"] == "Crusher":
                device_configs, device_nodedatas = modify_ESPSJ(device_configs,device_nodedatas,step["Parameters"])
            elif step["Equipment"] == "XRD":
                device_configs, device_nodedatas = modify_XRD(device_configs,device_nodedatas,step["Parameters"])
    submit_data = create_auto_lab_task_data(device_configs, device_nodedatas)
    response = submit_experiment_task(submit_data)
    print(response)
    return response

def workflow_extraction():

    five_prompt = ChatPromptTemplate.from_template(task_parse_prompt)

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, max_tokens=1000)
    llm_extraction_model = LLMChain(llm=llm, prompt=five_prompt)
    return llm_extraction_model
class Universal_task_Schema(BaseModel):

    task_workflow: str = Field(..., description="""It should be an exhaustive task flow, such as a material synthesis task.
    """)


class Universal_task_tool(BaseTool):
    name = "Universal_task_tool"
    description = "Very useful when you want to use automated labs to perform tasks."
    args_schema: Type[BaseModel] = Universal_task_Schema

    def _run(self, task_workflow) -> str:
        llm_extraction_model = workflow_extraction()
        print("here")
        bb = llm_extraction_model({"synthesis_processes": task_workflow})["text"].replace("```","").replace("json","")
        task_workflow = json.loads(bb)
        print(task_workflow)
        response = universal_task_submit(task_workflow)
        return response

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

