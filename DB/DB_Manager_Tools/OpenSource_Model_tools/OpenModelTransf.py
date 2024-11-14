from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.tools import BaseTool
from DB.DB_Manager_Tools.MIR_tools.Base.Data_loder import read_excel_data


def OpenModeltool(query: str, file_path: str):
    data = read_excel_data(file_path)
    return "Transfer learning has been completed."


class OpenModeltool_TraSchema(BaseModel):

    query: str = Field(description="It should be a model name, choosing the most appropriate one between the following three: 3D printed porous silicone rubber stress-strain model; 2D material adsorption energy model; CO2 adsorption model.")
    f_path: str = Field(description="Should be a dataset.")


class Open_Model_Tra(BaseTool):
    name = "Open_Model_transfer"
    description = "VVery useful when you want to use transfer learning."
    args_schema: Type[BaseModel] = OpenModeltool_TraSchema

    def _run(self, query: str, f_path: str) -> str:

        return OpenModeltool(query, f_path)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

