import streamlit as st
import json
from conditional_chains import get_response, rag_chains
from user_file_handling import file_handling
import setup

# Page configuration
st.set_page_config(
    page_title="MASTER RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Chat Assistant", "Manage RAG Chains", "Upload Documents"])

# Initialize session state variables if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role":"assistant",
            "content": "Assalamualaikum! How can I help you?"
        }
    ]

# Main Chat Assistant Page
if page == "Chat Assistant":
    st.title("MASTER RAG")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Ask me something...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(user_input)
                st.write(response)
                
                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": response
                })

# Manage RAG Chains Page
elif page == "Manage RAG Chains":
    st.title("Manage RAG Chains")

    # Display existing chains
    st.subheader("Existing RAG Chains")
    
    # Create a table of existing chains
    chains_data = []
    for chain in rag_chains:
        chains_data.append([chain["name"], chain["description"]])
    
    st.table({"Chain Name": [row[0] for row in chains_data], 
              "Description": [row[1] for row in chains_data]})

    # Form for adding new chain
    st.subheader("Create New RAG Chain")
    
    with st.form("new_chain_form"):
        chain_name = st.text_input("Chain Name", placeholder="Enter a unique name")
        chain_description = st.text_area("Description", placeholder="Describe what this chain handles")
        chain_prompt = st.text_area("System Prompt", 
                                   placeholder="Enter the system prompt for this chain")
        
        submit_button = st.form_submit_button("Create Chain")
        
        if submit_button:
            if not chain_name or not chain_description or not chain_prompt:
                st.error("All fields are required")
            elif chain_name in [chain["name"] for chain in rag_chains]:
                st.error(f"Chain '{chain_name}' already exists")
            else:
                # Create new chain
                new_chain = {
                    "name": chain_name,
                    "description": chain_description,
                    "prompt": chain_prompt
                }
                
                # Add to existing chains
                rag_chains.append(new_chain)
                
                # Save to file
                with open("rag-chains.json", "w") as file:
                    json.dump(rag_chains, file, indent=4)
                
                st.success(f"Chain '{chain_name}' created successfully!")
                st.rerun()  # Refresh the page to show updated chains

# Upload Documents Page
elif page == "Upload Documents":
    st.title("Upload Documents")
    
    st.write("Upload text files to be indexed in your RAG system.")
    
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    
    if uploaded_file is not None:
        # Create a unique filename
        filename = uploaded_file.name
        
        # Read and display file content
        file_content = uploaded_file.read().decode("utf-8")
        
        st.subheader("File Preview")
        st.text_area("Content", file_content, height=300)
        
        # Process file button
        if st.button("Process and Index Document"):
            with st.spinner("Processing document..."):
                response = file_handling(file_content)
                if response != True:
                     st.error(f"Error processing document")
                else:
                    st.success(f"Document '{filename}' processed and indexed successfully!")