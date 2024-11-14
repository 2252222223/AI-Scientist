from DB.DB_Manager_Tools.ME_tools.Q_A_system import QA_Conversation
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
from DB.Base.Available_Vector_Library import available_vectors
from config import CONFIG
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


def select_exist_vector(CONFIG,query, available_vectors):
    llm = ChatOpenAI(model_name=CONFIG["model_name"], temperature=0, max_tokens=1000)
    template_string = """Query: {query}
    Available areas: {available_vectors}

    Task:

    You are an expert in the field of materials science and your task is to identify whether a user query belongs to one of the following areas. Please note that you cannot simply make a judgement by capturing keywords, but you need to make a judgement based on materials science domain knowledge. This is because it is likely that the domain keywords will not appear directly in these queries.
    Return Address: If belong, return the name of the corresponding areas.Note,You can only reply to one of the Available areas in your response without additional explanation. For example: Li-rich
    Fallback: If no belong, return "No, no such areas exists." 
    """
    prompt = ChatPromptTemplate.from_template(template_string)
    Gpt = LLMChain(llm=llm, prompt=prompt)

    response = Gpt({"query": query, "available_vectors": available_vectors})
    return response



class DKSchema(BaseModel):
    query: str = Field(description="should be a professional issues related to {areas}.".format(areas=available_vectors))


class DKquery(BaseTool):
    name = "Domain_knowledge_query"
    description = """Useful when you need answers to questions related to {areas}. """.format(areas=available_vectors)
    args_schema: Type[BaseModel] = DKSchema

    def _run(self, query: str) -> str:
        key_word = select_exist_vector(CONFIG, query, available_vectors)["text"]
        print(key_word)

        if "No" in key_word.upper():
            return "The query does not belong to {areas} and needs to be answered using General_query.".format(areas=available_vectors)
        else:
            answer = QA_Conversation(query, key_word)
            return answer.get("summary_answer")

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")
