from pathlib import Path
from datetime import datetime
import os
def creat_path():
    # 获取当前脚本所在的路径
    script_dir = Path(__file__).resolve().parent
    # 获取当前时间并格式化为文件名
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 拼接文件路径
    filename = script_dir / 'expertise_save' / f'{current_time}.txt'
    # 创建并写入文件
    with open(filename, 'w') as file:
        file.write("")

    return filename

def exp_write(role:str, input:str, expert_experience_path:str,goal:bool= False):
    if not os.path.exists(expert_experience_path):
        with open(expert_experience_path, 'w') as file:
            if goal:
                context = "goal: " + input + "**\n"
            else:
                context = f"{role}: " + input +"**\n"
            file.write(context)
    else:
        with open(expert_experience_path, 'a') as file:
            if goal:
                context = "goal: " + input + "**\n"
            else:
                context = f"{role}: " + input +"**\n"
            file.write(context)


