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
ml_agent = Departmental_Manager_agent(CONFIG, ml_tools_list, Expert_experience_path=Expert_experience_path)


# class MLSchema(BaseModel):
#     query: str = Field(description="Query must contain two parts, objective: what you expect this subordinates to accomplish; file path: the dataset address, some tasks may contain multiple datasets, split by ','.")


class MLSchema(BaseModel):
    query: str = Field(description="Should be a dictionary. goal:what you expect this subordinates to accomplish, goal should include more details, such as specifying interpretable algorithms, and be sure to inform the components if they exist.;train_set:The address of the training set required by the objective for machine learning algorithm training.test_set:Optional, Addresses of other files needed for machine learning algorithms, such as test sets, candidate sets, validation sets, etc. Components: optional, information about the components involved in the task.")


class CustomMLTool(CEOBaseTool):
    name = "ML_tools_agent"
    description = "This is one of your subordinates who is very good at utilizing machine learning algorithms for a variety of tasks. "
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
# import langchain
#
# # print(CEO_agent.Expert_experience)
# langchain.debug = True
# ml_agent.run(["{'goal': 'Perform feature correlation analysis on the CO2 adsorption dataset', 'train_set': './CO2adsorption.xlsx'}"])

