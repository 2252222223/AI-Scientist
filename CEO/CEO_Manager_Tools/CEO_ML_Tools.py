#环境变量要设置到最前面，加载包的前面，不然无法传进去
import os
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
from CEO.Base.CEO_Basetool import CEOBaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from DB.Base.Manager_agent import Departmental_Manager_agent, CEO_to_Manager_parse
from DB.DB_Manager_Tools.MIR_tools.ML_TOOLS_integrated import ml_tools_list
from config import CONFIG
Expert_experience_path = "D:\pycharm\\MatterAI-0816-only-test\\DB\\DB_Manager_Tools\\ML_tools\\Expert_experience\\Expert_experience vector_store"
ml_agent = Departmental_Manager_agent(CONFIG, ml_tools_list, Expert_experience_path=Expert_experience_path,ai_name="MIR agent")


class MLSchema(BaseModel):
    query: str = Field(description="""
    It should have a dictionary-style structure. The goal keyspecifies the task to be accomplished and must include enough details such as the algorithm to be used, the dataset path with its description, and any other contextual details (e.g., combining knowledge with data reasoning).  For example:
    {
  "goal": "Here is a dataset of the composition and hardness of alloys, the dataset address is D:/alloy.xls, which is modeled using different machine learning algorithms (e.g., Random Forest, XGBOOST, Neural Networks)  to get the kind of algorithm with the highest accuracy."
    } 
    """)


class CustomMLTool(CEOBaseTool):
    name = "MIR_tools_agent"
    description = "This is one of your subordinates who is very good at utilizing machine learning algorithms for a variety of tasks. For example, material design, material reasoning, etc. "
    args_schema: Type[BaseModel] = MLSchema

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("Start Conver")
        print(query)
        query = str(query)
        query =CEO_to_Manager_parse(query)
        print("query:" + query)
        return ml_agent.run([query])

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
