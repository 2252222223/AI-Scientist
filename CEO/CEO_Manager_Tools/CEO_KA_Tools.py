from CEO.Base.CEO_Basetool import CEOBaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from CEO.Base.CEO_sk import sk
from DB.Base.Manager_agent import Departmental_Manager_agent, CEO_to_Manager_parse
from DB.DB_Manager_Tools.SL_tools.KA_TOOLS_integrated import ka_tools_list
from DB.Base.Available_Vector_Library import available_vectors
from pydantic import BaseModel, Field
from config import CONFIG
Expert_experience_path = "D:\pycharm\\MatterAI-0816\\DB\\DB_Manager_Tools\\Knowledge_Acquisition_tools\\Expert_experience\\Expert_experience vector_store"
ka_agent = Departmental_Manager_agent(CONFIG, ka_tools_list,Expert_experience_path = Expert_experience_path)


class CustomKAToolSchema(BaseModel):
      query: str = Field(description=  "It should be a dictionary where the input contains two parts, goal:The goals you want your subordinates to accomplish. It should be learning domain knowledge or pdf to txt conversion; f_path: Address where the literature is located. ")


class CustomKATool(CEOBaseTool):
    name = "Knowledge_Acquisition_agent"
    description = "Useful when users explicitly ask you to take knowledge from literature. "

    args_schema: Type[BaseModel] = CustomKAToolSchema

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query = CEO_to_Manager_parse(query)
        return ka_agent.run([query])

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
