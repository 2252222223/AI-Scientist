# -*- coding: utf-8 -*-
import os
#环境变量要设置到最前面，加载包的前面，不然无法传进去
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
import langchain
from CEO.Base.CEO_Basetool import CEOBaseTool

from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from DB.Base.Manager_agent import Departmental_Manager_agent, CEO_to_Manager_parse
from pydantic import BaseModel, Field
from DB.DB_Manager_Tools.Auto_Lab_tools.Auto_Lab_TOOLS_integrated import Auto_lab_tools_list
from config import CONFIG

Autolab_agent = Departmental_Manager_agent(CONFIG, Auto_lab_tools_list,ai_name="PEI agent")



class AutoLabSchema(BaseModel):
    goal: str = Field(description="Automated laboratory tasks that you want your subordinates to complete. If the task is a material synthesis task, the instructions must contain enough details about the material synthesis so that the subordinate properly understands the synthesis steps. For other tasks, the workflow must contain sufficient detail.")


class CustomAutoLabTool(CEOBaseTool):
    name = "Auto_lab_agent"
    description = "This is one of your subordinates, useful when you wish to utilise an automated lab for material synthesis and other task."
    args_schema: Type[BaseModel] = AutoLabSchema

    def _run(
            self, gaol: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query = CEO_to_Manager_parse(gaol)

        return Autolab_agent.run([query])
    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")

