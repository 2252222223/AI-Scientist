from fastapi import Body
from pathlib import Path
import uvicorn
import uuid
from Bo_api_val import TaskParams,get_task_params, read_file, vaild_train_can, vaild_params
from pydantic import Field
from time import sleep
import shutil
from fastapi.responses import FileResponse
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import Union
from DataProcessing import generate_candidate_space
import json
from GP_tool import active_learning


# 创建一个数据模型，用于定义请求体的结构和验证

class User_Input(BaseModel):
    query: str = Field(..., description="user input.")
    sequential_task_id: str = Field(..., description="Sequence task ids that track unique identifiers for long conversations.")


class Learning_Input(BaseModel):
    query: str = Field(..., description="user input.")
    sequential_task_id: str = Field(..., description="Sequence task ids that track unique identifiers for self_learning.")



app = FastAPI()

# 创建一个字典来存储任务的状态和结果
task_dict = {}

# a helper function to save the uploaded file to a local directory
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

# poscar to img
def poscar_to_img(current_task_id: str, filename: str):
    # 更新任务状态为运行中
    image_path = "./222.jpg"
    task_dict[current_task_id]["mid_result"] = FileResponse(image_path, media_type="image/jpeg")
    task_dict[current_task_id]["status"] = "running"
    print(task_dict)

# poscar to enery pre

def energy_pre(current_task_id: str, filename: str):
    sleep(20)
    task_dict[current_task_id]["status"] = "done"
    task_dict[current_task_id]["result"] = "4.58 eV"


# 定义一个后台任务函数，模拟一个耗时的操作
def GP_Bayesian_optimization(current_task_id: str, params: dict):
    # 更新任务状态为运行中
    task_dict[current_task_id]["status"] = "running"
    # 执行任务
    new_x, candidate_data_pred, lower_bound, upper_bound, acq_value, sorted_indices = active_learning(params)
    # 更新任务状态为完成，并设置结果
    record = {
        "current_task_id": current_task_id,
        "new_x": new_x.tolist(),
        "candidate_data_pred": candidate_data_pred.tolist(),
        "lower_bound": lower_bound.tolist(),
        "upper_bound": upper_bound.tolist(),
        "acq_value": acq_value.tolist(),
        "sorted_indices": sorted_indices.tolist()
    }

    task_dict[current_task_id]["status"] = "done"
    task_dict[current_task_id]["result"] = record

# 定义一个后台任务函数，模拟一个耗时的操作
def self_learning_task(current_task_id: str, sequential_task_id:str, query: str):
    # 更新任务状态为运行中
    task_dict[current_task_id]["status"] = "running"
    # 模拟耗时操作，这里用sleep代替
    sleep(10)
    # 更新任务状态为完成，并设置结果
    task_dict[current_task_id]["status"] = "done"
    if "electrolyte" in query:
        task_dict[current_task_id]["result"] = "Having searched and studied relevant papers, I have acquired knowledge of the subject area and we can discuss it further."
    else:
        task_dict[current_task_id]["result"] = "I apologize that I could not find the relevant papers in my literature library. We can discuss some other areas such as lithium-rich disordered cathode materials."


# a route to upload and save the POSCAR file
@app.post("/energypre")
def upload_poscar(background_tasks: BackgroundTasks, poscar: UploadFile = File(...)):
    # 生成一个随机的任务id
    current_task_id = str(uuid.uuid4())
    current_task_id_1 = str(uuid.uuid4())
    # 在字典中创建一个任务对象，初始状态为等待中
    task_dict[current_task_id] = {"status": "waiting", "result": None}
    task_dict[current_task_id_1] = {"status": "waiting", "result": None}
    # create a directory to store the files if not exists
    poscar_dir = Path("poscars")
    poscar_dir.mkdir(exist_ok=True)
    # save the poscar file to the directory
    save_upload_file(poscar, poscar_dir / poscar.filename)
    file_name = poscar.filename
    # 把后台任务函数添加到后台任务队列中，传入参数
    background_tasks.add_task(poscar_to_img, current_task_id, file_name)
    # 把后台任务函数添加到后台任务队列中，传入参数
    background_tasks.add_task(energy_pre, current_task_id_1, file_name)
    # 返回响应，告知用户任务id和状态
    return {"message": f"Current task {current_task_id} started.","current_task_id":current_task_id, "status": task_dict[current_task_id]["status"],"current_task_id_1":current_task_id_1, "status_1": task_dict[current_task_id_1]["status"]}



#返回图片
@app.get("/image")
async def get_image():
    image_path = "./222.jpg"
    return FileResponse(image_path)

@app.get("/start")
async def start_task():
    # 生成一个随机的任务id
    sequential_task_id = str(uuid.uuid4())
    # 返回响应，告知用户任务id和状态
    return {"message": f"The new sequential task was successfully created.", "sequential_task_id": sequential_task_id}

# 定义一个路由，用于接收用户的请求，并分配一个任务id
@app.post("/conversations")
async def start_task(background_tasks: BackgroundTasks, user_input: User_Input = Body(..., embed=True)):
    # 生成一个随机的任务id
    current_task_id = str(uuid.uuid4())
    # 在字典中创建一个任务对象，初始状态为等待中
    task_dict[current_task_id] = {"status": "waiting", "result": None}
    # 把后台任务函数添加到后台任务队列中，传入参数
    print(user_input)
    # background_tasks.add_task(conversations_task, current_task_id, user_input.sequential_task_id, user_input.query)
    # 返回响应，告知用户任务id和状态
    return {"message": f"Current task {current_task_id} started.", "current_task_id":current_task_id, "status": task_dict[current_task_id]["status"]}



@app.post("/bayesian_optimization")
async def start_task(background_tasks: BackgroundTasks,
                     train_data: UploadFile = File(..., description="With known data points, the input should be a table file and the label should be after the feature column.",),
                     candidate_space_file: Union[UploadFile, None] = File(default=None, description="tabular document. Unknown candidate space with feature columns to be aligned with known points."),
                     candidate_space_dict: Union[str, None] = Form(default=None, description="""json format,sunch as {"var1":(1,10,1),"var2":(10,100,5)}. in which, (start,end,step). Unknown candidate space with feature columns to be aligned with known points."""),
                     task_params: TaskParams = Depends(get_task_params)):


    if candidate_space_dict:
        candidate_space_dict = json.loads(candidate_space_dict)
        candidate_space = generate_candidate_space(candidate_space_dict)

    # 读取 train_data
    train_data = await read_file(train_data)
    # 读取 candidate_space
    if candidate_space_file:
        candidate_space = await read_file(candidate_space_file)
    candidate_space = await vaild_train_can(train_data, candidate_space,task_params)

    input_params = {"know_point": train_data, "candidate_space": candidate_space, "opt_direction": task_params.opt_direction, "opt_dim": task_params.opt_dim,
              "acq_function": task_params.acq_function, "feature_nums": len(train_data.columns)}

    await vaild_params(input_params)

    # 生成一个随机的任务id
    current_task_id = str(uuid.uuid4())
    # 在字典中创建一个任务对象，初始状态为等待中
    task_dict[current_task_id] = {"status": "waiting", "result": None}
    # 把后台任务函数添加到后台任务队列中，传入参数

    background_tasks.add_task(GP_Bayesian_optimization, current_task_id, input_params)
    # 返回响应，告知用户任务id和状态
    return {"message": f"Current task {current_task_id} started.", "current_task_id":current_task_id, "status": task_dict[current_task_id]["status"]}




@app.post("/self_learning")
async def start_task(background_tasks: BackgroundTasks, learning_input: Learning_Input = Body(..., embed=True)):
    # 生成一个随机的任务id
    current_task_id = str(uuid.uuid4())
    # 在字典中创建一个任务对象，初始状态为等待中
    task_dict[current_task_id] = {"status": "waiting", "result": None}
    # 把后台任务函数添加到后台任务队列中，传入参数
    background_tasks.add_task(self_learning_task, current_task_id, learning_input.sequential_task_id, learning_input.query)
    # 返回响应，告知用户任务id和状态
    return {"message": f"Current task {current_task_id} started.", "current_task_id":current_task_id, "status": task_dict[current_task_id]["status"]}

# 定义一个路由，用于查询任务的状态和结果
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    # 判断任务id是否存在于字典中
    print(task_id)
    if task_id in task_dict:
        # 返回响应，告知用户任务的状态和结果
        if str(task_dict[task_id]["result"]).endswith(".png"):
            return FileResponse(task_dict[task_id]["result"], media_type="image/jpeg")
        else:
            return {"status": task_dict[task_id]["status"], "result": task_dict[task_id]["result"]}
    else:
        # 返回响应，告知用户任务id无效
        return {"message": f"Invalid task id: {task_id}"}

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=9050)