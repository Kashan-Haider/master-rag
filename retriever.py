from pinecone_setup import connect_pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone_text.sparse import BM25Encoder
import pickle
import os
import json


# Save and load paths
BM25_MODEL_PATH = "bm25_model.pkl"

def load_bm25_model(path):
    with open(path, "rb") as f:
        model = pickle.load(f)
    print(f"BM25 model loaded from {path}")
    return model

def get_retriever(index_name: str, alpha: float) -> PineconeHybridSearchRetriever:
    index = connect_pinecone(index_name=index_name)

    # Load existing BM25 model if available
    if os.path.exists(BM25_MODEL_PATH):
        bm25_model = load_bm25_model(BM25_MODEL_PATH)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    retriever = PineconeHybridSearchRetriever(
        embeddings=embeddings,
        sparse_encoder=bm25_model,
        index=index,
        alpha=alpha,
        top_k=10,
        text_key="text"
    )

    return retriever




# Run a sample query
# retriever = get_retriever('test-index', 0.7)
# relevant_documents = retriever.invoke('i want a sedan car in white color')
# result = [doc.page_content for doc in relevant_documents]
# print(result)

# data = []
# with open('cars_data.json', 'r') as file:
#     data = json.load(file)
# print(data[0])
# retriever.add_texts(data[:1000])