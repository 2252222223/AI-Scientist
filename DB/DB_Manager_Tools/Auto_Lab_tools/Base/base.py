from datetime import datetime
import requests
from typing import Optional, Dict


base_url = ""

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