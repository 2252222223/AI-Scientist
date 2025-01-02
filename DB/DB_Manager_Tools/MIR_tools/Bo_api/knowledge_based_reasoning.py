import pandas as pd
import os
from config import CONFIG
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=40)


#知识推理
def LLM_decison_save(LLM_decison):
    # 文件名
    file_name = 'GPT4-decision.txt'
    # 要添加的文本
    text_to_add = LLM_decison + '\n'
    # 检查文件是否存在
    if os.path.isfile(file_name):
        # 文件存在，打开文件并追加文本
        with open(file_name, 'a') as file:
            file.write(text_to_add)
    else:
        # 文件不存在，创建文件并写入文本
        with open(file_name, 'w') as file:
            file.write(text_to_add)
def history_save(history,role,context):
    history += "\n" + role + ": " + context
    return history
Response_format = str({"previous_observations": "Finds the user's latest feedback from the conversation history and describes in detail if there has been an improvement, or None if there is no history of conversations.",
"explanation": "reasonable explanation for the next_suggestion",
"next_suggestion":"Give the next suggested component, which must come from Unknown space."
})
prompt_template = """You are AI.Your name is AI-Scientist.\
Now you act a professor in the field of material science.\
Your role is to help users design a Li-rich disordered cathode material with high initial capacity and high capacity retention based on known information, conversation history, and your knowledge of materials science.\
The entire process is a continuous iterative process, and your response needs to include the selection of the next component with a reasonable explanation, as well as a list of the user's observations of the results of the previous iteration.\
Note, You must select the next suggested component MUST come from the Unknown space provided by the user.\
Note, Mn(II), Mn(III), Mn(IV) represent 2-, 3-, and 4-valent Mn, respectively.

You should only respond in JSON format as described below: 
Response Format:{Response_format}

Make sure your response is parsed by json.load.\

Known information:{initial_value}.

Unknown space：{Unknown_space}

The following is the conversation history between user and You:
Conversation history:{history}.

Note,The next suggested component must come from unknown space.
Your response:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["Response_format","initial_value","history","Unknown_space"])

llm_model = ChatOpenAI(model_name = CONFIG["model_name"], temperature=0,max_tokens=1000)
GPT4_res = LLMChain(llm=llm_model, prompt=PROMPT)

def get_initial_value(path):
    # 假设你的表格文件是CSV格式，文件名为'data.csv'
    df = pd.read_excel(path)
    columns = df.columns
    # 生成字符串描述
    descriptions = []
    for _, row in df.iterrows():
        elements=[]
        for element in columns[:-2]:
            if row[element] != 0:
                elements.append(f"{element}{row[element]:.2f}")
        component = ''.join(elements)
        description = f"The initial capacity of {component} was {row[columns[-2]]:.2f} mah/g and 20th capacity retention was {row[columns[-1]]:.2f}%"
        descriptions.append(description)
    return ',\n'.join(descriptions)

def get_next_unkonw_value(unknow_space):
    df = unknow_space.iloc[:100].sample(30)
    # 生成字符串描述
    columns = df.columns
    descriptions = []
    for _, row in df.iterrows():
        elements=[]
        for element in columns:
            if row[element] != 0:
                elements.append(f"{element}{row[element]:.3f}")
        alloys = ''.join(elements)
        description = f"{alloys}"
        descriptions.append(description)
    return ',\n'.join(descriptions)