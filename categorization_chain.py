from dotenv import load_dotenv
import os
import json

load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
rag_chains = []
with open("rag-chains.json", "r") as file:
    rag_chains = json.load(file)

chain_names = [entry["name"] for entry in rag_chains]
formatted_chain_names = ", ".join(chain_names)



# Modify the prompt to instruct the LLM to output JSON.
prompt = ChatPromptTemplate(
    [
        (
            "system",
            (
                "You are a helpful AI that classifies user queries into predefined topics. "
                "You will be given a list of topics and a user query. Your task is to identify which topic "
                "from the list the query belongs to. If the query doesn’t match any topic, respond with 'default'. "
                "Return your answer a single category like 'cars', 'medical', 'movies'.\nTopics:\n{chain_names}"
            ),
        ),
        ("human", "{user_input}"),
    ]
)

categorizationChain = prompt | llm

# user_input = input("Prompt : ")
# result = categorizationChain.invoke({"chain_names": chain_names, 'user_input': user_input})

# print(result.content)
