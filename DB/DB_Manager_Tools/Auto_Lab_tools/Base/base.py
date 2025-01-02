from datetime import datetime
import requests
from typing import Optional, Dict


base_url = "http://matterai.e3.luyouxia.net:12427"

import time

# 获取当前时间的毫秒数
def get_time():
    timestamp_ms = int(time.time() * 1000)
    return timestamp_ms

def get_current_time():
    """
    获取当前时间并格式化为 'YYYY/MM/DD HH:MM:SS' 格式。

    返回:
    str: 格式化后的当前时间字符串。
    """
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

def Temperature_parise(Temperature_set): #[{"temperature_start":0,"temperature_end":1000,"time":100}, {"temperature_start":1000,"temperature_end":1000,"time":600}, {"temperature_start":1000,"temperature_end":20,"time":100}]
    temperature = []
    for i in Temperature_set:
        a = {"key": get_time(),
             "time": i["time"],
             "temperature": i["temperature_end"],
             "speed": int((i["temperature_end"] - i["temperature_start"])/i["time"])}
        temperature.append(a)
    #田间最后一行
        last = {"key": get_time(),
                "time": -121,
                "temperature": 30,
                "speed":0}





def auth_login(phone: str, password: str, client_type: str = "Robot_Server",
               base_url = base_url):
    """
    封装 HTTP GET 请求以进行用户登录认证。

    参数:
    phone (str): 用户的手机号。
    password (str): 用户的密码。
    client_type (str): 客户端类型，默认为 "Robot_Server"。

    返回:
    dict: 请求的响应结果（JSON 格式）。
    """
    # 构建请求的 URL
    suffix_url = "/api/User/AuthLogin"
    url = base_url + suffix_url
    params = {
        "phone": phone,
        "password": password,
        "clientType": client_type
    }

    try:
        # 发起 GET 请求
        response = requests.get(url, params=params)
        # 检查 HTTP 响应状态码
        response.raise_for_status()
        # 返回 JSON 格式的响应内容
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

def get_token():
    result = auth_login(phone="13812340001", password="123456")
    print(result)
    if result["msg"] == "登录成功":
        token = result["token"]["access_token"]
        return token

token = get_token()


# 提交实验任务
def sumbit_expertiment_task(suffix_url: str, token: str, data: dict,
                            base_url: str = base_url):
    # 构建请求的 Headers
    url = base_url + suffix_url
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"  # 指定为 JSON 格式
    }

    try:
        # 发起 POST 请求
        response = requests.post(url, headers=headers, json=data)
        # 检查 HTTP 响应状态码
        response.raise_for_status()
        # 返回 JSON 格式的响应内容
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None


def auto_lab_request_post(suffix_url: str, data: Optional[dict] = None, token = token, base_url=base_url):

    # 构建请求的 Headers
    url = base_url + suffix_url
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"  # 指定为 JSON 格式
    }
    try:
        # 发起 POST 请求
        # 根据 data 是否为 None 决定是否发送请求体
        if data:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers)
        # 检查 HTTP 响应状态码
        response.raise_for_status()
        # 返回 JSON 格式的响应内容
        return response.json()

    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None


def modify_experimental_parameters(device_configs: list, device_nodedatas: list,devices_all_parameters: dict, modify_parameters: Optional[dict]= None):
    if modify_parameters is not None:
        for k, v in modify_parameters.items():
            devices_all_parameters["data"][k] = modify_parameters[k]
    nodedata = {"NodeId": devices_all_parameters["id"],
                    "NodeName": devices_all_parameters["name"],
                    "NodeCreateTime": get_current_time()}
    device_configs.append(devices_all_parameters)
    device_nodedatas.append(nodedata)
    return device_configs, device_nodedatas


def get_drug_setting():
    return auto_lab_request_post(suffix_url="/api/Experiment/drug_setting")

task_parse_prompt="""
You are the manager of a materials synthesis laboratory. Your task is to analyze detailed synthesis processes provided by users and convert them into executable steps based on the equipment available in the lab.

Task Requirements:
1. Maintain the order of the process as described by the user.
2. For each step, identify the experimental parameters. If no specific parameters are provided, return None.
3. Select only the equipment you need.
4. Return the output as a valid JSON object that can be parsed by json.load().
5. Only json is returned, additional interpretation is forbidden.
6. The output is represented as a list of dictionaries, each containing three key-value pairs:
    Step: Ordering of steps. It should start with 1.
    Equipment: The name of the equipment.
    Parameters : Equipment input parameters.
    Example:[
    "Step":1,
    "Equipment": "Powder Loading Systems",
    "Parameters": [
    {{"drug_name": "Li2CO3", "mass": 280}},
    {{"drug_name": "MnO", "mass": 100}},
    {{"drug_name": "Mn2O3", "mass": 150}},
    {{"drug_name": "TiO2", "mass": 50}},
    {{"drug_name": "LiF", "mass": 30}}
    ]
    ]


Laboratory Equipment Available:
1. Powder Loading Systems: Used to weigh and load solid precursors into a container. Operating parameters are represented as a list of dictionaries with:
    drug_name: Chemical formula of the precursor.
    mass: Weight of the precursor (mg). 
    Example:
    [
      {{"drug_name": "Li2CO3", "mass": 280}},
      {{"drug_name": "Li2F", "mass": 30}}
    ]
2.Liquid Injection Systems: Used to add liquid precursors. Operating parameters are represented as a list of dictionaries with:

    liquid_name: Chemical formula of the liquid.
    volume: Volume of the liquid (ml). 
    Example: [
      {{"liquid_name": "H2O", "volume": 20}},
      {{"liquid_name": "C2H5OH", "volume": 30}}
    ]
3. Ball Mill: Used to mix reaction precursors. Operating parameters are represented as a dictionaries with:
    running_time: Duration (seconds).
    running_speed: Speed (integer between 0 and 1500, default 1200). 
    Example: {{
      "running_time": 600,
      "running_speed": 1200
    }}
4. Tube Furnace: Used for high-temperature sintering. Operating parameters are represented as a dictionaries with:
    start_temperature: Starting temperature (°C).
    target_temperature: Target temperature (°C).
    time: Duration (minutes). Note: The first stage must start at 0°C and each subsequent stage must start at the previous stage's target temperature. 
    Example:[
      {{"start_temperature": 0, "target_temperature": 100, "time": 10}},
      {{"start_temperature": 100, "target_temperature": 200, "time": 15}}
    ]
5. Oven: Used for liquid-phase reactions or drying, with temperatures below 200°C. Operating parameters are represented as a dictionaries with:
    temperature: Operating temperature (°C, max 200).
    time: Holding time (minutes). 
    Example:
    {{
      "temperature": 150,
      "time": 300
    }}
6. Tablet Press: Used to press powders into tablets. This device has no configurable parameters.
7. Crusher: Used to pulverize samples into powder. This device has no configurable parameters.
8. XRD: Used for physical characterization. Parameters are:
    samplename: Name of the sample.
    highvoltagekv: Optional voltage (10-40 kV, default 30).
    highvoltagema: Optional current (5-40 mA, default 20). 
    Example:
    {{
      "samplename": "Li2MnO3",
      "highvoltagekv": 20
    }}

User input:
{synthesis processes}
"""