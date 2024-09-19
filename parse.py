# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate



# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return an empty string ('')."
#     "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
# )

# model = OllamaLLM(model="llama3.1")


# def parse_with_ollama(dom_chunks,parse_description):
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model

#     parsed_result = []

#     for i, chunk in enumerate(dom_chunks,start =1):
#         response = chain.invoke(
#             {"dom_content" : chunk, "parse_description": parse_description}
#                                               )
        
#         print (f"Parsed batch {i} of {len(dom_chunks)}")
#         parsed_result.append(response)

#     return "\n".join(parsed_result)


#due to slower response time from ollama running locally the new code uses google's gemini 1.5 flash and groq APIs to get quicker response



from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import os

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def get_model(model_name):
    if model_name == "groq":
        return ChatGroq(
            temperature=0,
            groq_api_key=os.environ["GROQ_API_KEY"],
            model_name="mixtral-8x7b-32768"
        )
    elif model_name == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            google_api_key=os.environ["GOOGLE_API_KEY"]
        )
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def parse_with_llm(dom_chunks, parse_description, model_name):
    prompt = ChatPromptTemplate.from_template(template)
    model = get_model(model_name)
    chain = prompt | model

    parsed_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_result.append(response.content)

    return "\n".join(parsed_result)