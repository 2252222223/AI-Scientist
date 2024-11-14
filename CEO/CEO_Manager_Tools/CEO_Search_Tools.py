from langchain.tools import BaseTool
from CEO.Base.CEO_Basetool import CEOBaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from CEO.Base.CEO_sk import sk, search_key
import os
from DB.Base.Manager_agent import Departmental_Manager_agent
from langchain.agents import load_tools
os.environ["SERPAPI_API_KEY"] = search_key



ser_tools = load_tools(["serpapi"])
ser_agent = Departmental_Manager_agent(sk,ser_tools)


class CustomSerTool(CEOBaseTool):
    name = "Search_tools_agent"
    description = "useful for when you need to answer questions about Li-ion battery. NOTE: Tasks must be related to lithium-ion batteries in order to be used."
#     args_schema: Type[BaseModel] = CalculatorInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return ser_agent.run([query])

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")