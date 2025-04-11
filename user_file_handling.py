from retriever import get_retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

def file_handling(file_content):
    try:
        # Get retriever
        retriever = get_retriever("test-index", 0.7)

        # Split content into chunks (simplified approach)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        chunks = text_splitter.split_text(file_content)

        # Add to index
        retriever.add_texts(chunks)
        print("upserted data")
        return True

    except Exception as e:
        print(e)
        return False
