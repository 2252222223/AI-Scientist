from langchain.tools import BaseTool
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.Submit_task import submit_experiment_task, create_auto_lab_task_data
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.Devices import get_XRD_all_parameters
from DB.DB_Manager_Tools.Auto_Lab_tools.Base.base import get_current_time
from pydantic import BaseModel, Field, conint
from typing import Optional, Type
import json

class XRD_Schema(BaseModel):
    XRD_parameters: str = Field(..., description="Should be a dictionary containing XRD parameters. samplename:Name of the sample.testsampletype:Optional parameter, default is 2, Values: 0 (Nickel sheet), 1 (Ceramic sheet), 2 (Powder). highvoltagekv:ptional parameter, testing tube voltage, range: 10-40, default: 30. highvoltagema:Optional parameter, testing tube current, range: 5-40, default: 20.")


def XRD_task_submit(XRD_parameters) -> str:
    XRD_all_parameters = get_XRD_all_parameters()
    for k, v in XRD_parameters.items():
        XRD_all_parameters["data"][k] = XRD_parameters[k]

    device_configs = [XRD_all_parameters]
    XRD_nodedata = {"NodeId": XRD_all_parameters["id"],
   "NodeName": XRD_all_parameters["name"],
   "NodeCreateTime": get_current_time()}
    device_nodedatas =[XRD_nodedata]

    submit_data = create_auto_lab_task_data(device_configs,device_nodedatas)
    response = submit_experiment_task(submit_data)
    print(response)
    return response


class XRD_tool(BaseTool):
    name = "XRD_tool"
    description = "Very useful when you want to characterise materials using XRD."
    args_schema: Type[BaseModel] = XRD_Schema

    def _run(self, XRD_parameters) -> str:

        print("here")
        XRD_parameters = json.loads(XRD_parameters)
        print(XRD_parameters)
        return XRD_task_submit(XRD_parameters)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")
