from CEO.Base.CEO_Basetool import CEOBaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from CEO.Base.CEO_sk import sk
from DB.Base.Manager_agent import Departmental_Manager_agent, CEO_to_Manager_parse
from DB.DB_Manager_Tools.DA_tools.Data_Collect_TOOLS_integrated import Data_Collect_tools_list
from pydantic import BaseModel, Field
from typing import Optional, Type
from config import CONFIG
from langchain.tools import BaseTool


Expert_experience_path = "D:\pycharm\\MatterAI-0816\\DB\\DB_Manager_Tools\\Data_Collect_tools\\Expert_experience\\Expert_experience vector_store"
DC_agent = Departmental_Manager_agent(CONFIG, Data_Collect_tools_list,Expert_experience_path = Expert_experience_path)


class DatacollectPreSchema(BaseModel):

    query: str = Field(description="The query should contain two parts, the first part is the characteristics of the data you want to collect and the second part is the address of the document in text format.")


class CustomDataCollectTool(CEOBaseTool):
    name = "Data_Collect_tools_agent"
    description = "Very useful when you need to collect datasets from the literature."
    args_schema: Type[BaseModel] = DatacollectPreSchema

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query = CEO_to_Manager_parse(query)
        return DC_agent.run([query])

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")


