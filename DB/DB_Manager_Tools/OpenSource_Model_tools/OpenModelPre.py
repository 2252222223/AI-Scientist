from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.tools import BaseTool
from DB.DB_Manager_Tools.MIR_tools.Base.Data_loder import read_excel_data
from DB.DB_Manager_Tools.OpenSource_Model_tools.Silicone_rubber import rubber_stress_strain_predict


def OpenModeltool_Pre(query: str, file_path: str):
    if query == "3D printed porous silicone rubber stress-strain model":

        pre_save_path = rubber_stress_strain_predict(file_path)
        return f"Stress-strain curve prediction is completed and its prediction data is saved in {pre_save_path}."


class OpenModeltool_PreSchema(BaseModel):
    query: str = Field(description="It should be a model name, choosing the most appropriate one between the following three: 3D printed porous silicone rubber stress-strain model; 2D material adsorption energy model; CO2 adsorption model.")
    f_path: str = Field(description="Should be the address of a tabular data file to be predicted.")


class Open_Model_Pre(BaseTool):
    name = "Open_Model_Predict"
    description = "Very useful when you need open source models for prediction."
    args_schema: Type[BaseModel] = OpenModeltool_PreSchema

    def _run(self, query: str, f_path: str) -> str:

        return OpenModeltool_Pre(query, f_path)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

