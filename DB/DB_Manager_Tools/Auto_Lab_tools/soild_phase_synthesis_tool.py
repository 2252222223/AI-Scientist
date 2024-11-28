from langchain.tools import BaseTool
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.Submit_task import submit_experiment_task, create_auto_lab_task_data
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.Devices import (get_XRD_all_parameters,get_WLDWT_all_parameters,
                                                             get_GTLPF_all_parameters,get_QMGYW_all_parameters,
                                                             get_SGKGJ_all_parameters,get_QMGQMJ_all_parameters,
                                                             get_RQZH_all_parameters, get_TCYPJ_all_parameters,
                                                             get_GTLHCGW_all_parameters,get_GSL_all_parameters,
                                                             get_ESPSJ_all_parameters)
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.base import get_current_time,modify_experimental_parameters
from pydantic import BaseModel, Field, conint
from typing import Optional, Type
import json



def solid_synthesis_task_submit(solid_synthesis_parameters) -> str:
    device_configs = []
    device_nodedatas = []
    #物料定位台取高通量料架
    WLDWT_all_parameters_1 = get_WLDWT_all_parameters()
    WLDWT_modify_parameters_1 = {}
    WLDWT_modify_parameters_1["selContainer"] =4
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      WLDWT_all_parameters_1, WLDWT_modify_parameters_1)

    #高通量配分系统
    GTLPF_all_parameters_1 = get_GTLPF_all_parameters()
    GTLPF_modify_parameters_1 = {"materialCup1_Status": True,  # 1号料杯 是否启用
    "materialCup1_Tank1_Status": True,  # 1号料杯1号罐是否启用
    "materialCup1_Tank1_Weight": "300",  # 1号料杯-1号料罐 加多少mg的药品
    "materialCup1_Tank2_Status": True,  # 1号料杯2号罐是否启用
    "materialCup1_Tank2_Weight": "300",  # 1号料杯-2号料罐 加多少mg的药品
    "materialCup1_Tank3_Status": True,
    "materialCup1_Tank3_Weight": "200",
    "materialCup1_Tank4_Status": False,
    "materialCup1_Tank4_Weight": 0,
    "materialCup1_Tank5_Status": False,
    "materialCup1_Tank5_Weight": 0,
    }
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,GTLPF_all_parameters_1, GTLPF_modify_parameters_1)
    #球磨罐移位
    QMGYW_all_parameters_1 = get_QMGYW_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      QMGYW_all_parameters_1)
    #试管开盖机锁盖
    SGKGJ_all_parameters_1 = get_SGKGJ_all_parameters()
    SGKGJ_modify_parameters_1 = {}
    SGKGJ_modify_parameters_1["operate"]= 1
    SGKGJ_modify_parameters_1["selectContainer"] = 2
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      SGKGJ_all_parameters_1, SGKGJ_modify_parameters_1)
    #球磨罐球磨机
    QMGQMJ_all_parameters_1 = get_QMGQMJ_all_parameters()
    QMGQMJ_runing_time = solid_synthesis_parameters["ball_mill"]["runing_time"]
    QMGQMJ_runing_speed = solid_synthesis_parameters["ball_mill"]["runing_spend"]
    QMGQMJ_modify_parameters_1 = {}
    QMGQMJ_modify_parameters_1["loopNumber"] = min(int(QMGQMJ_runing_time/360), 15)
    QMGQMJ_modify_parameters_1["speed_1"] = QMGQMJ_runing_speed
    QMGQMJ_modify_parameters_1["speed_2"] = QMGQMJ_runing_speed
    QMGQMJ_modify_parameters_1["speed_3"] = QMGQMJ_runing_speed
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      QMGQMJ_all_parameters_1, QMGQMJ_modify_parameters_1)
    #试管开盖机开盖
    SGKGJ_all_parameters_2 = get_SGKGJ_all_parameters()
    SGKGJ_modify_parameters_2 = {}
    SGKGJ_modify_parameters_2["operate"]= 0
    SGKGJ_modify_parameters_2["selectContainer"] = 2
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      SGKGJ_all_parameters_2, SGKGJ_modify_parameters_2)
    #物料定位台拿新的球磨罐，过滤钢珠
    WLDWT_all_parameters_2 = get_WLDWT_all_parameters()
    WLDWT_modify_parameters_2 = {}
    WLDWT_modify_parameters_2["selContainer"] = 2
    WLDWT_modify_parameters_2["container2Position"] = 9 #1到8是坩埚，9到16是球磨罐
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      WLDWT_all_parameters_2, WLDWT_modify_parameters_2)
    #物料转换，过滤钢珠
    RQZH_all_parameters_1 = get_RQZH_all_parameters()
    RQZH_modify_parameters_1 = {}
    RQZH_modify_parameters_1["operate"] = 2 #球磨罐转球磨罐
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      RQZH_all_parameters_1, RQZH_modify_parameters_1)
    #物料定位台取坩埚
    WLDWT_all_parameters_3 = get_WLDWT_all_parameters()
    WLDWT_modify_parameters_3 = {}
    WLDWT_modify_parameters_3["selContainer"] = 2
    WLDWT_modify_parameters_3["container2Position"] = 1 #1到8是坩埚，9到16是球磨罐
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      WLDWT_all_parameters_3, WLDWT_modify_parameters_3)

    #陶瓷压片机
    TCYPJ_all_parameters_1 = get_TCYPJ_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      TCYPJ_all_parameters_1)

    #高通量缓存工位
    GTLHCGW_all_parameters_1 = get_GTLHCGW_all_parameters()
    GTLHCGW_modify_parameters_1 = {}
    GTLHCGW_modify_parameters_1["selectContainer"] = 3 #坩埚
    GTLHCGW_modify_parameters_1["robotTaskType"] = 2  #放
    GTLHCGW_modify_parameters_1["selectPostion"] = 4  #取
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GTLHCGW_all_parameters_1, GTLHCGW_modify_parameters_1)

    #高通量缓存工位
    GTLHCGW_all_parameters_2 = get_GTLHCGW_all_parameters()
    GTLHCGW_modify_parameters_2 = {}
    GTLHCGW_modify_parameters_2["selectContainer"] = 3 #坩埚
    GTLHCGW_modify_parameters_2["robotTaskType"] = 1  #取
    GTLHCGW_modify_parameters_2["selectPostion"] = 5  #全部取
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GTLHCGW_all_parameters_2, GTLHCGW_modify_parameters_2)

    #管式炉[{"start":0,"end":1000,"time":100}, {"start":1000,"end":1000,"time":600}, {"start":1000,"end":20,"time":100}]
    Temperature_set = solid_synthesis_parameters["tube_furnace"]
    Temperature_modify_parameters = []
    for i in Temperature_set:
        single_stage = {}
        single_stage["key"] = ""
        single_stage["time"] = i["time"]
        single_stage["temperature"] = i["target_temperature"]
        single_stage["speed"] = 0
        Temperature_modify_parameters.append(single_stage)

    GSL_all_parameters = get_GSL_all_parameters()
    GSL_modify_parameters_1 ={}
    GSL_modify_parameters_1["param"] = Temperature_modify_parameters
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GSL_all_parameters, GSL_modify_parameters_1)


    #高通量缓存工位 放料
    #高通量缓存工位
    GTLHCGW_all_parameters_3 = get_GTLHCGW_all_parameters()
    GTLHCGW_modify_parameters_3 = {}
    GTLHCGW_modify_parameters_3["selectContainer"] = 3 #坩埚
    GTLHCGW_modify_parameters_3["robotTaskType"] = 2  #放
    GTLHCGW_modify_parameters_3["selectPostion"] = 5  #全部
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GTLHCGW_all_parameters_3, GTLHCGW_modify_parameters_3)

    #高通量缓存工位 取1个
    GTLHCGW_all_parameters_4 = get_GTLHCGW_all_parameters()
    GTLHCGW_modify_parameters_4 = {}
    GTLHCGW_modify_parameters_4["selectContainer"] = 3 #坩埚
    GTLHCGW_modify_parameters_4["robotTaskType"] = 1  #取
    GTLHCGW_modify_parameters_4["selectPostion"] = 4  #
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      GTLHCGW_all_parameters_4, GTLHCGW_modify_parameters_4)
    #鳄式破碎机
    ESPSJ_all_parameters = get_ESPSJ_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      ESPSJ_all_parameters)
    #XRD
    XRD_all_parameters = get_XRD_all_parameters()
    device_configs, device_nodedatas = modify_experimental_parameters(device_configs, device_nodedatas,
                                                                      XRD_all_parameters)
    submit_data = create_auto_lab_task_data(device_configs, device_nodedatas)




    # response = submit_experiment_task(submit_data)
    # print(response)
    # return response

class solid_synthesis_Schema(BaseModel):
    solid_synthesis_parameters: str = Field(..., description="""Please output the synthesis parameters in the following JSON format. 
    Ensure that the format is valid and can be parsed by json.load(). 
    1. solid_phase_synthesis_process_parameters: The top-level key should contain the synthesis process parameters in JSON format.
    2. ball_mill: (Optional) The ball mill working parameters, represented as a dictionary. The dictionary should include:
    running_time: The running time of the ball mill, in seconds (integer).
    running_speed: The running speed of the ball mill, an integer between 0 and 1500. Default value is 1200 if not provided.
    example: "ball_mill": {
    "running_time": 600,
    "running_speed": 1200
    }
    3. tube_furnace: (Optional) The tube furnace temperature parameters, represented as a list of dictionaries. Each dictionary should contain three keys:
    start_temperature: The starting temperature (integer, °C).
    target_temperature: The target temperature (integer, °C).
    time: The duration of the heating phase in minutes (integer)
    example："tube_furnace": [
    {
        "start_temperature": 0,
        "target_temperature": 100,
        "time": 10
    },
    {
        "start_temperature": 100,
        "target_temperature": 200,
        "time": 15
    }
    ]
    Important Notes:
    The start_temperature of the first stage must be 0°C.
    For subsequent stages, the start_temperature must be equal to the target_temperature of the previous stage.
    """)


class Solid_synthesis_tool(BaseTool):
    name = "solid_synthesis_tool"
    description = "Very useful when you need to synthesise materials using solid phase burning."
    args_schema: Type[BaseModel] = solid_synthesis_Schema

    def _run(self, solid_synthesis_parameters) -> str:

        print("here")
        solid_synthesis_parameters = json.loads(solid_synthesis_parameters)
        print(solid_synthesis_parameters)
        return solid_synthesis_task_submit(solid_synthesis_parameters)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")