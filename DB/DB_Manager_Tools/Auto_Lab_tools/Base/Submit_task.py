from DB.DB_Manager_Tools.Auto_Lab_tools.Base.base import auto_lab_request_post
from typing import Optional, Dict, List, Any

#创建任务编号


def create_task_number(suffix_url: str ="/api/Experiment/CreateExperimentNumber"):

    response = auto_lab_request_post(suffix_url)

    return response["data"]


# 提交实验任务
def submit_experiment_task(data: dict, suffix_url: str ="/api/Record/SubmitExperimentRecord"):

    response = auto_lab_request_post(suffix_url,data)

    return response


#创建提交数据
def create_auto_lab_task_data(device_configs: List[Dict[str, Any]], device_nodedatas: List[Dict[str, Any]]):
    task_id = create_task_number()
    exp_name = "AI-sumbit-" + task_id
    data = {"ExpRecordData": {"Name": exp_name,
                              "Number": task_id,
                              "Status": "10",
                              "ExpectedWorkingHours": 1,
                              "Sort": 1,
                              "ExpStartTime": None,
                              "ExpEndTime": None,
                              "FlowPathConfig": "",
                              "Remark": ""},
            "NodeConfigData": device_configs,
            "ExpConfigNodeData": device_nodedatas}

    return data
