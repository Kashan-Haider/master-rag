from pinecone_setup import connect_pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import PineconeHybridSearchRetriever
import pickle
import os

BM25_MODEL_PATH = "bm25_model.pkl"

# Load pre-trained BM25 model from disk
def load_bm25_model(path):
    with open(path, "rb") as f:
        model = pickle.load(f)
    print(f"BM25 model loaded from {path}")
    return model

# Returns a hybrid retriever combining dense and sparse search
def get_retriever(index_name: str, alpha: float) -> PineconeHybridSearchRetriever:
    index = connect_pinecone(index_name=index_name)

    bm25_model = None
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

