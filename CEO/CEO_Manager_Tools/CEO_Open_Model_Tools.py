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


Expert_experience_path = "D:\pycharm\\MatterAI-0816\\DB\\DB_Manager_Tools\\Knowledge_Q_A_tools\\Expert_experience" \
                         "\\Expert_experience vector_store "
Open_model_agent = Departmental_Manager_agent(CONFIG, Open_model_tools_list,Expert_experience_path = Expert_experience_path)


class OpenModelSchema(BaseModel):
    query: str = Field(description="Should be a dictionary. goal: the task you expect this subordinate to accomplish; train_set: Optional, the address of the training set required by the goal for transfer learning.")


class CustomOpenModelTool(CEOBaseTool):
    name = "Open_model_agent"
    description = "This is one of your subordinates whose very good at using trained models for prediction or transfer learning."
    args_schema: Type[BaseModel] = OpenModelSchema

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query = CEO_to_Manager_parse(query)
        print("query:" + query)

        return Open_model_agent.run([query])

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
