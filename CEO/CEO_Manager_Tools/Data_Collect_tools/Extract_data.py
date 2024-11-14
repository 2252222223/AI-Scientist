from langchain.chat_models import ChatOpenAI
from CEO.Base.CEO_sk import sk
from kor.nodes import Object, Text, Number
from kor.extraction import create_extraction_chain
from langchain.prompts import PromptTemplate


def creat_exrract_chain(materials_name ,attributes):
    material_schema = Object(
        id="material",
        description="Information about a material",
        # Notice I put multiple fields to pull out different attributes
        attributes=attributes,
        many = False
    )
    materials_name_number = len(materials_name.split("|"))
    materials_name_split = ",".join(materials_name.split("|"))
    five_template = """You are a data scientist in the field of materials science \
        and your goal is to collect datasets that can be used for machine learning training. \
        Your now goal is to extract structured information from the user's input \
        that matches the form described below. \
        NOTE,The users' input contains {materials_name_number} materials,{materials_name}.\
        When extracting information please make sure \
        it matches the type information exactly. Do not add any attributes that do not appear \
        in the schema shown below.\
        NOTE,If this attributes is not found,YOU MUST OUTPUT None.

        {type_description}

        {format_instructions} 

        """
    five_template = five_template.format(materials_name_number = materials_name_number
                                         ,materials_name = materials_name_split ,type_description="{type_description}"
                                         ,format_instructions="{format_instructions}")
    instruction_template = PromptTemplate(
        input_variables=["type_description", "format_instructions"],
        template=five_template
    )
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0, max_tokens=1000, openai_api_key=sk)
    chain = create_extraction_chain(llm, material_schema, instruction_template=instruction_template, encoder_or_encoder_class="csv")
    return chain
