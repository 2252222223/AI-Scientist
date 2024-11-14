from CEO.Base.CEO_Basetool import CEOBaseTool

from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from CEO.Base.CEO_sk import sk
from DB.Base.Manager_agent import Departmental_Manager_agent, CEO_to_Manager_parse
from DB.Base.Available_Vector_Library import available_vectors
from pydantic import BaseModel, Field
from DB.DB_Manager_Tools.OpenSource_Model_tools.OpenModel_TOOLS_integrated import Open_model_tools_list
from config import CONFIG





class AutoLabSchema(BaseModel):
    query: str = Field(description="Should be a dictionary. goal: The material synthesis task you want this subordinate to complete. The instructions must contain enough details about the material synthesis so that the subordinate can properly understand the synthesis steps.")


class CustomAutoLabTool(CEOBaseTool):
    name = "Auto_lab_agent"
    description = "This is one of your subordinates, useful when you wish to utilise an automated lab for material synthesis."
    args_schema: Type[BaseModel] = AutoLabSchema

    def _run(
            self, gaol: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query = CEO_to_Manager_parse(gaol)
        print("query:" + query)

        return "Because of the security risks associated with the publication of the code for remote calls from the lab's automated lab, the material synthesis task could not be performed."

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
