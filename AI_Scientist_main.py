from langchain.chat_models import ChatOpenAI
import os
#环境变量要设置到最前面，加载包的前面，不然无法传进去
from CEO.Base.CEO_sk import sk,api_base,search_key
os.environ['OPENAI_API_KEY'] = sk
os.environ["OPENAI_API_BASE"] = api_base
os.environ["SERPAPI_API_KEY"] = search_key
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore import InMemoryDocstore
from CEO.Base.CEO_Auto_gpt import CEO_GPT
import faiss
from langchain.vectorstores import FAISS
from CEO.CEO_Manager_Tools.CEO_Manger_Tool_integrated import CEO_tools_list



def memory_store():
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
    return vectorstore

tools = CEO_tools_list

vectorstore = memory_store()



Expert_experience_path = "E:\pycharm\\MatterAI-0816-only-test\\CEO\\CEO_Manager_Tools\\Expert_experience\\Expert_experience vector_store"


def AI_Scientist(CONFIG):
    llm = ChatOpenAI(model_name=CONFIG["model_name"], temperature=0, max_tokens=1000)
    CEO_agent = CEO_GPT.from_llm_and_tools(
        ai_name="the CEO",
        ai_role="you need to organize your subordinates to collaborate in accomplishing goal.",
        tools=CONFIG["tools"],
        llm=llm,
        memory=vectorstore.as_retriever(search_kwargs={"k": 8}),
        Expert_experience = Expert_experience_path,  # 设置专家经验数据库地址
        Expert_experience_switch= CONFIG["Expert_experience_switch"],
        COB_in_the_loop= CONFIG["COB_in_the_loop"],  # Set to True if you want to add feedback at each step.
        feedback_tool = CONFIG["interaction_manager"]
    )
    return CEO_agent

import langchain

# print(CEO_agent.Expert_experience)
langchain.debug = True
#
# query = """"""
#
# CEO_agent.run([query])
