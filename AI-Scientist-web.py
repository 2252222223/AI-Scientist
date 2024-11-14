import threading
import queue
from config import CONFIG
import random
import gradio as gr
import time
from CEO.Base.COB_intervention import COBInputRun, InteractionManager
from AI_Scientist_main import AI_Scientist
from CEO.CEO_Manager_Tools.CEO_Manger_Tool_integrated import CEO_departments_huamn_choice,available_departments
# from Agent_test import Agent
from css import title_html
from config import CONFIG
# 新增一个全局变量，用于追踪是否已重置
reset_flag = False

interaction_manager = CONFIG["interaction_manager"]
def monitor(chat_history):
    global reset_flag

    # print(reset_flag)
    # 如果刚刚执行过重置，则跳过读取旧消息
    if reset_flag:
        chat_history.clear()
        reset_flag = False  # 重置标志，下一次可以继续正常监控消息队列
        # print(chat_history)
        return chat_history

    # 处理用户输入的显示
    if not interaction_manager.user_queue.empty():
        user_message = interaction_manager.user_queue.get()
        chat_history.append((user_message, None))  # 用户输入消息

    # 处理机器回复的显示
    if not interaction_manager.output_queue.empty():
        output_message = interaction_manager.output_queue.get()
        chat_history.append((None, output_message))  # 机器回复
    # print(chat_history)
    return chat_history


# 用户输入处理函数，将输入传递给交互管理器
def user_input_fn(user_input):
    interaction_manager.receive_input(user_input)
    return ""

# 启动Agent线程
def agent_thread_func(goals):
    interaction_manager.receive_goal(goals)
    agent.run([goals])
    # 初始化交互管理器和Agent

def start_task(goals,selected_tools):
    print(selected_tools)
    global interaction_manager, agent
    interaction_manager = CONFIG["interaction_manager"]
    ceo_tools = CEO_departments_huamn_choice(selected_tools)
    CONFIG["tools"] = ceo_tools
    agent = AI_Scientist(CONFIG)
    agent_thread = threading.Thread(target=agent_thread_func, args=(goals,))
    agent_thread.start()

# 刷新按钮处理函数
def reset_game(chatbot,goals,selected_tools):
    global interaction_manager, agent, reset_flag
    reset_flag = True  # 标志重置操作

    # 清空交互管理器的队列
    interaction_manager.user_queue = queue.Queue()
    interaction_manager.output_queue = queue.Queue()

    # 重新初始化交互管理器和Agent
    interaction_manager = CONFIG["interaction_manager"]
    ceo_tools = CEO_departments_huamn_choice(selected_tools)
    CONFIG["tools"] = ceo_tools
    agent = AI_Scientist(CONFIG)
    agent_thread = threading.Thread(target=agent_thread_func, args=(goals,))
    agent_thread.start()

    # 清空聊天记录
    chatbot = []
    return chatbot, "", "" # 返回清空的chat_history
tool_options = list(available_departments.keys())
def AI_Scientist_UI():
    # 构建Blocks上下文，并应用 CSS
    with gr.Blocks() as demo:
        # 将标题设置为 Markdown 并应用自定义类
        gr.Markdown(title_html)
        with gr.Row():
            tools_choices = gr.CheckboxGroup(
                label="Choose Tools",
                choices= tool_options,
                type="value",
            )
        with gr.Row():
            goals = gr.Textbox(label="goal：", lines=1,scale=5)
            goals_submit = gr.Button("🚀 提交", scale=1)
            refresh_button = gr.Button("✨ 新任务", scale=1)
        with gr.Row():
            # 输出显示框，应用自定义CSS类
            chatbot = gr.Chatbot()
        with gr.Row():
            input_box = gr.Textbox(label="用户输入：", lines=1,scale=5)
            submit_button = gr.Button("🚀 提交", scale=1)

        with gr.Row():
            train_file = gr.File(label="训练集")  # 返回的是文件，用文件名可获得地址
            can_space_file = gr.File(label="未知空间")
        submit_button.click(fn=user_input_fn, inputs=[input_box], outputs=[input_box])
        refresh_button.click(fn=reset_game,inputs=[chatbot,goals,tools_choices],outputs=[chatbot, input_box])
        goals_submit.click(fn = start_task, inputs=[goals,tools_choices],outputs = None)
        demo.load(fn=monitor, inputs=[chatbot], outputs=[chatbot], every=1.0)
    return demo

demo = AI_Scientist_UI()
demo.queue(concurrency_count=10, status_update_rate=1, max_size=30)
demo.launch()


