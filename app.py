import streamlit as st
import json
from conditional_chains import get_response, rag_chains
from user_file_handling import file_handling
import nltk

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

st.set_page_config(
    page_title="MASTER RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("MASTER RAG")
    st.markdown("---")
    st.subheader("Navigation")
    page = st.radio(
        "",
        ["Chat Assistant", "Manage RAG Chains"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("RAG-powered AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Assalamualaikum! How can I help you?"}
    ]

if page == "Chat Assistant":
    st.title("Chat Assistant")

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(
                message["role"], avatar="🧠" if message["role"] == "assistant" else "👤"
            ):
                st.write(message["content"])

    user_input = st.chat_input("Ask me something...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user", avatar="👤").write(user_input)

        with st.spinner("Generating response..."):
            response = get_response(user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()


elif page == "Manage RAG Chains":
    st.title("Manage RAG Chains")

    st.subheader("Existing RAG Chains")
    if not rag_chains:
        st.info("No RAG chains found. Create your first chain below.")
    else:
        for chain in rag_chains:
            with st.expander(f"📚 {chain['name']}"):
                st.markdown(f"**Description:** {chain['description']}")
                st.markdown("---")
                st.caption("System Prompt Preview (first 100 chars)")
                st.text(
                    chain["prompt"][:100] + "..."
                    if len(chain["prompt"]) > 100
                    else chain["prompt"]
                )

    st.subheader("Create New RAG Chain")

    with st.form("new_chain_form", clear_on_submit=False):
        chain_name = st.text_input("Chain Name", placeholder="Enter a unique name")
        chain_description = st.text_area(
            "Description", placeholder="Describe what this chain handles", height=100
        )
        chain_prompt = st.text_area(
            "System Prompt",
            placeholder="Enter the system prompt for this chain",
            height=200,
        )

        submit_button = st.form_submit_button("Create Chain")

        if submit_button:
            if not chain_name or not chain_description or not chain_prompt:
                st.error("All fields are required")
            elif chain_name in [chain["name"] for chain in rag_chains]:
                st.error(f"Chain '{chain_name}' already exists")
            else:
                new_chain = {
                    "name": chain_name,
                    "description": chain_description,
                    "prompt": chain_prompt,
                }
                rag_chains.append(new_chain)
                with open("rag-chains.json", "w") as file:
                    json.dump(rag_chains, file, indent=4)
                st.success(f"Chain '{chain_name}' created successfully!")

                # ✅ Save state to keep showing uploader after form submit
                st.session_state["created_chain_name"] = chain_name

    # ✅ Show file uploader if a chain was just created
    if "created_chain_name" in st.session_state:
        st.subheader("Upload Documents for: " + st.session_state["created_chain_name"])
        uploaded_file = st.file_uploader("Choose a text file", type="txt")

        if uploaded_file is not None:
            filename = uploaded_file.name
            file_content = uploaded_file.read().decode("utf-8")
            st.subheader("File Preview")
            st.text_area("Content", file_content, height=300)

            if st.button("Process and Index Document"):
                with st.spinner("Processing document..."):
                    response = file_handling(file_content)
                    if response != True:
                        st.error("Error processing document")
                    else:
                        st.success(
                            f"Document '{filename}' processed and indexed successfully!"
                        )
                        st.balloons()
                        # Optionally clear the flag
                        del st.session_state["created_chain_name"]
                        st.rerun()
