import gradio as gr
import pandas as pd
from GP_tool import active_learning
from DataProcessing import generate_candidate_space
# 创建一个带有 HTML 和 CSS 的标题
title_html = """
    <h1 style="text-align: center; font-size: 30px;">MatterAI for BO</h1>
"""

def process_inputs(train_file,opt_dim,opt_direction,acq_function,can_space_file = None, can_space_form = None):
    train_data = pd.read_excel(train_file.name)
    if can_space_file:
        candidate_space= pd.read_excel(can_space_file.name)
    if can_space_form["特征名"][0] !="":
        # 如果 can_space_form 是 DataFrame 类型，执行相关操作
        can_dict = {}
        for i in range(len(can_space_form)):
            can_dict[can_space_form["特征名"][i]]= [float(can_space_form["起点"][i]),float(can_space_form["终点"][i]),float(can_space_form["步长"][i])]
        print(can_dict)
        candidate_space = generate_candidate_space(can_dict)
    params = {"know_point": train_data, "candidate_space": candidate_space, "opt_direction": opt_direction, "opt_dim": int(opt_dim),
              "acq_function": acq_function, "feature_nums": len(train_data.columns)}
    new_x, candidate_data_pred, lower_bound, upper_bound, acq_value, sorted_indices = active_learning(params)

    return new_x[0]

def clear_input():
    return None, None, None, "", None, None,

def Bo_UI():
    # 构建Blocks上下文
    with gr.Blocks() as demo:
        gr.Markdown(title_html)
        with gr.Row():    # 列排列
            train_file = gr.File(label="上传已知点数据集")#返回的是文件，用文件名可获得地址
            can_space_file = gr.File(label="上传未知候选空间")
            can_space_form = gr.DataFrame(label='候选空间生成', col_count = (4, 'fixed'),headers=["特征名","起点","终点","步长"],interactive=True, wrap=True)
        with gr.Row():
            opt_dim = gr.Text(label="优化维度：", lines=1)
            opt_direction = gr.Dropdown(choices=["max","min"],label="优化方向：")
            acq_function = gr.Dropdown(choices=["EI","UCB","PI","qEHVI","qNEHVI"],label="采集函数：")
        with gr.Row():
            submit_button = gr.Button("🚀 提交")
            clean_button = gr.Button("🧹 清除")
        output = gr.Textbox(label="下一步探索点：")
        # 当点击提交按钮时，调用 process_inputs 函数
        submit_button.click(fn=process_inputs, inputs=[train_file,opt_dim,opt_direction,acq_function,can_space_file,can_space_form], outputs=output)
        clean_button.click(fn=clear_input, inputs=[], outputs=[train_file, can_space_file, can_space_form,opt_dim,opt_direction,acq_function])
    return demo
# demo.launch()



