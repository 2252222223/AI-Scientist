import os
import json
import numpy as np
import pandas as pd
from DB.DB_Manager_Tools.Data_Collect_tools.Gnerate_query import generate_query
from DB.DB_Manager_Tools.Data_Collect_tools.Feature_jason import generate_attributes
from DB.DB_Manager_Tools.Data_Collect_tools.Find_materials import find_materials
from DB.DB_Manager_Tools.Data_Collect_tools.Match_text import match_text
from DB.DB_Manager_Tools.Data_Collect_tools.Extract_data import creat_exrract_chain
from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.tools import BaseTool


def printOutput(output):
    print(json.dumps(output, sort_keys=True, indent=3))


def data_collect(chain, context):
    output = chain.run()["data"]
    printOutput(output)
    return output


#读取当前文件夹所有pdf
def all_file_name(file_dir, source_type=".txt"):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == source_type:
                z = file.split(".")
                L.append(file_dir + "/" + os.path.splitext(file)[0] + source_type)
                        #     print(L)
    return L


def df_Filter(df, materials_name):
    delet_index = []
    df.index = range(len(df))
    df = df.replace(r'-+', np.nan, regex=True)
    df = df.replace(" None", np.nan)
    df = df.replace("None", np.nan)
    for index, row in df.iterrows():
        # 统计每行的”None“的个数
        none_count = row.isna().sum()
        # 如果大于5，则删除该行
        if none_count > 3:
            delet_index.append(index)
    df = df.drop(delet_index)
    if "(" in materials_name:
        aaa = materials_name.split("|")
        for i in aaa:
            name = i.split(" (")[0].lstrip().rstrip()
            abbr = i.split(" (")[1].replace(")", "").lstrip().rstrip()
            print(abbr, name)
            df = df.replace(abbr, name)
    return df


def single_collect_data(new_dataset, exrract_chain, docs, materials_name):
    for i in range(3):
        context = docs[i].page_content
        aaa = data_collect(exrract_chain, context)
        df = pd.DataFrame(aaa["material"])
        if len(df.columns) == 1:
            sita= len(new_dataset)
            new_dataset.loc[sita,df.columns[0].split(":")[0].lstrip()]=df.columns[0].split(":")[1].lstrip()
            for index, row in df.iterrows():
                a = row.values[0].split(":")
                new_dataset.loc[sita, a[0].lstrip()] = a[1].lstrip()
        elif len(df.columns) == len(new_dataset.columns):
            new_dataset = pd.concat((new_dataset,pd.DataFrame(aaa["material"])), axis=0)
        new_dataset = df_Filter(new_dataset, materials_name)
    return new_dataset


def collect_data(query: str, file_path: str):
    L = all_file_name(file_path, source_type=".txt")
    print(L)
    attributes, materials_feature = generate_attributes(query)
    new_dataset = pd.DataFrame(columns=list(materials_feature.keys()))
    for i in range(len(L)):
        path = L[i]
        materials_name = find_materials(path)
        second_llm_output = generate_query(materials_name, query)
        docs = match_text(path, second_llm_output)
        exrract_chain = creat_exrract_chain(materials_name, attributes)
        new_dataset2 = single_collect_data(new_dataset, exrract_chain, docs, materials_name)
        new_dataset = pd.concat((new_dataset, new_dataset2), axis=0, ignore_index=True)
    new_dataset.to_csv("./data_collect.csv", index=False)
    return "Data collection from the literature has been completed and the dataset is saved at ./data_collect.csv"


class Data_collect_PreSchema(BaseModel):

    query: str = Field(description="Should be a query that contains the attributes of the data you want to collect.")
    f_path: str = Field(description="Should be the address of the literature in txt format.")


class Data_Collect(BaseTool):
    name = "Data_collect"
    description = "Very useful when you need to collect data from the literature."
    args_schema: Type[BaseModel] = Data_collect_PreSchema

    def _run(self, query: str, f_path: str) -> str:

        return collect_data(query, f_path)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

