
from typing import Callable, Optional
from Expert_experience_digitization_module.expertise_save import creat_path
from pydantic import Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
import threading
import queue
from Expert_experience_digitization_module.expertise_save import creat_path, exp_write


def _print_func(text: str) -> None:
    print("\n")
    print(text)




class COBInputRun(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "COB command"
    description = (
        "It is used for human COBs to send out the highest level of instructions."
    )
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        self.prompt_func(query)
        return self.input_func()

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human tool asynchronously."""
        raise NotImplementedError("Human tool does not support async")



#for web UI


class InteractionManager:
    def __init__(self, expertise_save: bool = False):
        self.output_queue = queue.Queue()  # 用于存储机器输出的队列
        self.input_queue = queue.Queue()  # 用于存储用户输入到Agent的队列
        self.user_queue = queue.Queue()  # 用于存储用户输入消息以显示的队列
        self.input_event = threading.Event()  # 控制Agent暂停和继续
        if expertise_save:
            self.exp_save_path = creat_path()
            self.exp_save = True
        else:
            self.exp_save = False
    def display_output(self, message):
        """将AI-Scientist回复放入输出队列"""
        role = "AI-Scientist:"
        if self.exp_save:
            exp_write(role, message, self.exp_save_path)
        self.output_queue.put(message)

    def run(self, prompt):
        """请求用户输入，暂停并等待用户反馈"""
        self.display_output(prompt)
        self.input_event.wait()  # 暂停Agent，等待用户输入
        self.input_event.clear()  # 清除事件
        return self.input_queue.get()  # 返回用户输入

    def receive_input(self, user_input):
        """接收用户输入并唤醒等待的Agent"""
        role = "COB:"
        if self.exp_save:
            exp_write(role, user_input, self.exp_save_path)
        self.input_queue.put(user_input)  # 将输入传递给Agent
        self.user_queue.put(user_input)   # 将用户输入放入用户队列
        self.input_event.set()  # 恢复暂停的Agent

    def receive_goal(self, goal):
        exp_write("", goal, self.exp_save_path,goal = True)