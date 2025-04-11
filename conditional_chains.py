from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from categorization_chain import categorizationChain, rag_chains, chain_names, llm
from retriever import get_retriever

index_name = "test-index"


def get_category(inputs):
    user_input = inputs["user_input"]
    context = inputs["context"]
    category = categorizationChain.invoke(
        {"chain_names": chain_names, "user_input": user_input}
    )
    print(category.content)
    return {"category": category.content, "user_input": user_input, "context": context}


chains = {}

for entry in rag_chains:
    if entry["name"] != "default":
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        entry["prompt"]
                        + "\n\nYou are a highly knowledgeable and reliable assistant, optimized to provide accurate, insightful, and actionable responses."
                        "\nRespond *exclusively* based on the information provided in the context below:\n{context}\n"
                        "You may summarize, rephrase, or logically organize the context to make your answer clearer and more helpful."
                        "\nAvoid speculation, assumptions, or introducing external knowledge."
                        "\nIf the context does not contain sufficient information to answer the query, respond by stating that explicitly."
                    ),
                ),
                ("human", "{query}"),
            ]
        )
    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an helpul ai assistant.tell the user that you're not specially trained for it but still you can help them out and then help them",
                ),
                ("human", "{query}"),
            ]
        )

    chain = prompt | llm
    chains[entry["name"]] = chain


def route_by_category(inputs):
    category = list({inputs["category"]})[0]
    user_query = inputs["user_input"]
    if category in chains:
        print("Running " + category)
        return chains[category].invoke(
            {"query": user_query, "context": inputs["context"]}
        )
    return chains["default"].invoke({"query": user_query})


full_chain = RunnableLambda(get_category) | RunnableLambda(route_by_category)


def get_response(user_input: str):
    retriever = get_retriever(index_name, 0.7)
    relevant_documents = retriever.invoke(user_input)
    context = [doc.page_content for doc in relevant_documents]
    response = full_chain.invoke({"user_input": user_input, "context": context})
    return response.content
