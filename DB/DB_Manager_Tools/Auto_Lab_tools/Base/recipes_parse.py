import pandas as pd
import re

def get_lab_reagents_dict():
    Reagents = pd.read_excel("D:\OneDrive - mails.ucas.ac.cn\Code\E707\AI-Scientist\DB\DB_Manager_Tools\Auto_Lab_tools\Base\Laboratory Reagents List.xlsx")
    Reagents_list = {}
    for index,row in Reagents.iterrows():
        Reagents_list[row["Reagents"]] = {"Purity":row["Purity"],"Molar mass":row["Molar mass"],"Metal source":row["Metal source"]}
    return Reagents_list

def prase_formula(formula):
    # 使用正则表达式匹配元素和它们的组分
    matches = re.findall(r'([A-Z][a-z]?\(?\w*\)?)(\d+\.\d+)', formula)
    # 将匹配结果转换为字典
    composition = {element: float(amount) for element, amount in matches}
    return composition

def parse_reagents_formula(formula):
    # 使用正则表达式匹配元素和它们的数量
    matches = re.findall(r'([A-Z][a-z]?)(\d*\.\d+|\d*)', formula)
    # 创建字典，如果没有指定数量，则默认为1
    element_dict = {match[0]: float(match[1]) if match[1] else 1 for match in matches}
    return element_dict

def recipes_to_descriptions(recipes):
    descriptions = []
    for k, v in recipes.items():
        description = f"{v:.3f}g {k}"
        descriptions.append(description)

    return ', '.join(descriptions)

def get_recipes(abc):
    Reagents_list = get_lab_reagents_dict()
    materials= abc["Chemical formula"]
    composition = prase_formula(materials)
    recipes = {}
    for ele,con in composition.items():
        if ele != "O":
            pre = abc["Precursor"][ele]
            #解析元素在药品中的占比
            pre_composition = parse_reagents_formula(pre)
            if "," not in Reagents_list[pre]["Metal source"]:
                recipes[pre] = con/pre_composition[ele.split("(")[0]]*Reagents_list[pre]['Molar mass']/Reagents_list[pre]['Purity']
            else:
                metal_source_split = Reagents_list[pre]["Metal source"].split(",")
                for source in metal_source_split:
                    if source == ele:
                        recipes[pre] = con/pre_composition[ele.split("(")[0]]*Reagents_list[pre]['Molar mass']/Reagents_list[pre]['Purity']
                    else:
                        pre = abc["Precursor"][source]
                        recipes[pre] = recipes[pre]/composition[source]*(composition[source]-con/pre_composition[ele.split("(")[0]])
    masses = 0
    for k,v in recipes.items():
        masses += v
    ratio = abc["Mass"]/masses
    for k,v in recipes.items():
        if k == "Li2CO3":
            recipes[k] = v*ratio*1.1
        else:
            recipes[k] = v*ratio
    mass = abc["Mass"]
    des = recipes_to_descriptions(recipes)
    des = f"{mass}g {materials} detailed recipe for the preparation is "  + des + "."
    return des

# abc ={
# "Chemical formula":"'Li1.200Mn(II)0.004Mn(III)0.714Ti0.150O1.950F0.050",
# "Precursor":{"Li":"Li2CO3","Mn(II)":"MnO","Mn(III)":"Mn2O3","Mn(IV)":"MnO2","Ti":"TiO2","Nb":"Nb2O5","F":"LiF"},
# "Mass":1
# }
#
# print(get_recipes(abc))