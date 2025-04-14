# Master RAG 🧠

A powerful RAG (Retrieval Augmented Generation) system that intelligently routes user queries to specialized knowledge domains.

## Overview

Master RAG is an advanced chatbot application that combines multiple domain-specific RAG chains with intelligent query categorization. The system automatically determines the appropriate knowledge domain for a user query and retrieves relevant information from a vector database before generating a response.

Key features:
- 🤖 Automatic query categorization
- 📚 Support for multiple specialized RAG chains
- 🔄 User-friendly interface to create new knowledge domains
- 📝 Document processing and indexing capabilities
- 🔍 Hybrid vector search using Pinecone

## Architecture

The project is built with the following components:

- **Streamlit Frontend**: User-friendly interface for chatting and managing RAG chains
- **Query Categorization**: Uses Google's Gemini model to classify user queries
- **Conditional Chaining**: Routes queries to specialized RAG chains based on categorization
- **Vector Database**: Pinecone for efficient similarity search and retrieval
- **Embeddings**: Hugging Face's MiniLM model for dense vector embeddings
- **Sparse Encoding**: BM25 algorithm for keyword-based retrieval
- **Hybrid Search**: Combines dense and sparse embeddings for optimal retrieval

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Pinecone API key
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/master-rag.git
cd master-rag
```

2. Install dependencies:
```bash
pip install .
```

3. Create a `.env` file in the project root with your API keys:
```
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_api_key
```

### Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```

## Using Master RAG

### Chat Assistant
- Navigate to the "Chat Assistant" tab to interact with the AI
- Type your query in the chat input and get intelligent responses

### Managing RAG Chains
- Go to the "Manage RAG Chains" tab to view and create knowledge domains
- Create a new chain by providing:
  - Chain Name: Unique identifier for the knowledge domain
  - Description: What kind of queries this chain handles
  - System Prompt: Instructions for the LLM when responding to these queries
- After creating a chain, upload text documents to index for that knowledge domain

## Project Structure

- `app.py`: Streamlit application
- `conditional_chains.py`: Main logic for routing queries to appropriate chains
- `categorization_chain.py`: Query classification using Gemini
- `retriever.py`: Interface with Pinecone for hybrid search
- `pinecone_setup.py`: Database connection and index management
- `user_file_handling.py`: Document processing and indexing
- `rag-chains.json`: Configuration for specialized knowledge domains

## Example Use Cases

- **Automotive Domain**: Find second-hand cars based on specific requirements
- **Medical Information**: Answer health-related queries with accurate information
- **Default Handler**: Gracefully handle queries outside of specialized domains

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
