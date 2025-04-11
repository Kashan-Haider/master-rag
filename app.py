import streamlit as st
import json
from conditional_chains import get_response, rag_chains
from user_file_handling import file_handling
import nltk

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

# Page configuration
st.set_page_config(
    page_title="MASTER RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    .subheader {
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    .chat-container {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation with better styling
with st.sidebar:
    st.markdown(
        "<h2 style='text-align: center; color: #fff;'>MASTER RAG</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("<h3 style='color: #4B5563;'>Navigation</h3>", unsafe_allow_html=True)
    page = st.radio(
        "",
        ["Chat Assistant", "Manage RAG Chains", "Upload Documents"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #4B5563; font-size: 0.8rem;'>RAG-powered AI Assistant</p>",
        unsafe_allow_html=True,
    )

# Initialize session state variables if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Assalamualaikum! How can I help you?"}
    ]

# Main Chat Assistant Page
if page == "Chat Assistant":
    st.markdown("<h1 class='main-header'>Chat Assistant</h1>", unsafe_allow_html=True)

    # Create a container for the chat with a light background
    chat_container = st.container()
    with chat_container:
        st.markdown(
            "<div class='chat-container' style='background-color: #F9FAFB;'>",
            unsafe_allow_html=True,
        )

        # Display chat history with better formatting
        for message in st.session_state.chat_history:
            with st.chat_message(
                message["role"], avatar="🧠" if message["role"] == "assistant" else "👤"
            ):
                st.write(message["content"])

        st.markdown("</div>", unsafe_allow_html=True)

    # User input
    user_input = st.chat_input("Ask me something...")

    # In the Chat Assistant page section:

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Display the chat history (including the new user message)
    for message in st.session_state.chat_history:
        with st.chat_message(
            message["role"], avatar="🧠" if message["role"] == "assistant" else "👤"
        ):
            st.write(message["content"])

    # Generate the response in a placeholder outside the chat history display
    with st.spinner("Generating response..."):
        response = get_response(user_input)

    # Add the response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Rerun to refresh the display with the new complete history
    st.rerun()
# Manage RAG Chains Page
elif page == "Manage RAG Chains":
    st.markdown(
        "<h1 class='main-header'>Manage RAG Chains</h1>", unsafe_allow_html=True
    )

    # Display existing chains
    st.markdown(
        "<h2 class='subheader'>Existing RAG Chains</h2>", unsafe_allow_html=True
    )

    if not rag_chains:
        st.info("No RAG chains found. Create your first chain below.")
    else:
        # Create a more visually appealing display of existing chains
        col1, col2 = st.columns(2)

        for i, chain in enumerate(rag_chains):
            with st.expander(f"📚 {chain['name']}"):
                st.markdown(f"**Description:** {chain['description']}")
                st.markdown("---")
                st.caption("System Prompt Preview (first 100 chars)")
                st.text(
                    chain["prompt"][:100] + "..."
                    if len(chain["prompt"]) > 100
                    else chain["prompt"]
                )

    # Form for adding new chain with better styling
    st.markdown(
        "<h2 class='subheader'>Create New RAG Chain</h2>", unsafe_allow_html=True
    )

    with st.form("new_chain_form", clear_on_submit=False):
        st.markdown(
            "<p style='color: #4B5563;'>Fill in the details to create a new RAG chain.</p>",
            unsafe_allow_html=True,
        )

        chain_name = st.text_input("Chain Name", placeholder="Enter a unique name")
        chain_description = st.text_area(
            "Description", placeholder="Describe what this chain handles", height=100
        )
        chain_prompt = st.text_area(
            "System Prompt",
            placeholder="Enter the system prompt for this chain",
            height=200,
        )

        cols = st.columns([3, 1])
        with cols[1]:
            submit_button = st.form_submit_button("✨ Create Chain")

        if submit_button:
            if not chain_name or not chain_description or not chain_prompt:
                st.error("⚠️ All fields are required")
            elif chain_name in [chain["name"] for chain in rag_chains]:
                st.error(f"⚠️ Chain '{chain_name}' already exists")
            else:
                # Create new chain
                new_chain = {
                    "name": chain_name,
                    "description": chain_description,
                    "prompt": chain_prompt,
                }

                # Add to existing chains
                rag_chains.append(new_chain)

                # Save to file
                with open("rag-chains.json", "w") as file:
                    json.dump(rag_chains, file, indent=4)

                st.success(f"✅ Chain '{chain_name}' created successfully!")
                st.balloons()
                st.rerun()  # Refresh the page to show updated chains

# Upload Documents Page
elif page == "Upload Documents":
    st.markdown("<h1 class='main-header'>Upload Documents</h1>", unsafe_allow_html=True)

    st.markdown(
        """
    <p style='margin-bottom: 20px; color: #4B5563;'>
        Upload text files to be indexed in your RAG system for improved responses.
    </p>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            "<div style='background-color: #F9FAFB; padding: 20px; border-radius: 10px;'>",
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader("Choose a text file", type="txt")

        if uploaded_file is not None:
            # Create a unique filename
            filename = uploaded_file.name

            # Read and display file content
            file_content = uploaded_file.read().decode("utf-8")

            st.markdown(
                "<h2 class='subheader'>File Preview</h2>", unsafe_allow_html=True
            )
            st.text_area("Content", file_content, height=300)

            # Process file button with better styling
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Process and Index Document", use_container_width=True):
                    with st.spinner("Processing document..."):
                        response = file_handling(file_content)
                        if response != True:
                            st.error(f"⚠️ Error processing document")
                        else:
                            st.success(
                                f"✅ Document '{filename}' processed and indexed successfully!"
                            )
                            st.balloons()

        else:
            st.info("📄 Drag and drop a text file here or click to browse")

        st.markdown("</div>", unsafe_allow_html=True)
