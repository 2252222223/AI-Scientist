import os
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
from CEO.Base.CEO_Basetool import CEOBaseTool

from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from CEO.Base.CEO_sk import sk
from DB.DB_Manager_Tools.ME_tools.Knowledge_Q_A_TOOLS_integrated import K_Q_A_tools_list
from DB.Base.Manager_agent import Departmental_Manager_agent, CEO_to_Manager_parse
from DB.Base.Available_Vector_Library import available_vectors
from pydantic import BaseModel, Field
from config import CONFIG

Expert_experience_path = "D:\pycharm\\MatterAI-0816\\DB\\DB_Manager_Tools\\Knowledge_Q_A_tools\\Expert_experience" \
                         "\\Expert_experience vector_store "
K_Q_A_agent = Departmental_Manager_agent(CONFIG, K_Q_A_tools_list,Expert_experience_path = Expert_experience_path)


class QASchema(BaseModel):
    query: str = Field(description="Should be a question in the field of materials.")


class CustomKQATool(CEOBaseTool):
    name = "k_Q_A_agent"
    description = "This is one of your subordinates who is very good at answering questions in the field of materials " \
                  "science. The tool has the highest priority in answering questions."

    args_schema: Type[BaseModel] = QASchema

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query = CEO_to_Manager_parse(query)
        print("query:" + query)

        return K_Q_A_agent.run([query])

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")


# K_Q_A_agent.run(["What are the aspects of fluoride ion doping that affect the performance of lithium-rich cathode materials?"])