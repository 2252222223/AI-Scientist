from DB.DB_Manager_Tools.Auto_Lab_tools.Base.recipes_parse import get_recipes
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, conint
from typing import Optional, Type
import json


class Recipes_Schema(BaseModel):
    Recipes_parameters: str = Field(..., description=""" The input, represented as a dictionary. The dictionary should include:
    Chemical formula: Chemical formula of the material.
    Precursor: material constituent elements and the corresponding precursors. Should be a dictionary with key as the element and value as the corresponding precursor.
    Mass: Mass of the synthesized material, default is 1.
    example: {
    "Chemical formula":"'Li1.200Mn(II)0.004Mn(III)0.714Ti0.150O1.950F0.050",
    "Precursor":{"Li":"Li2CO3","Mn(II)":"MnO","Mn(III)":"Mn2O3","Mn(IV)":"MnO2","Ti":"TiO2","Nb":"Nb2O5","F":"LiF"},
    "Mass":1
    }
    """)


class Recipes_tool(BaseTool):
    name = "Recipes_tool"
    description = "Very useful when you want to know the mass of various precursors added to lithium battery cathode materials."
    args_schema: Type[BaseModel] = Recipes_Schema

    def _run(self, Recipes_parameters) -> str:

        print("here")
        Recipes_parameters = json.loads(Recipes_parameters)
        print(Recipes_parameters)
        return get_recipes(Recipes_parameters)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")