import streamlit as st
import os
from loader import load_repo, clone_repo
from store import create_texts, build_collection
from brain import answer_question
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"
DB_PATH = BASE_DIR / "db"

st.set_page_config(page_title="Code RAG Explorer", page_icon="💻")
st.title("🚀 AI Code RAG Explorer")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repo_indexed" not in st.session_state:
    st.session_state.repo_indexed = False

with st.sidebar:
    st.header("Settings")
    git_link = st.text_input("GitHub Repository URL", placeholder="https://github.com/...")
    
    if st.button("Index Repository"):
        if git_link:
            with st.spinner("Cloning Repository..."):
                clone_repo(git_link, local_dir=DATA_PATH/"repo")
                docs = load_repo(DATA_PATH)
                texts = create_texts(docs)
                st.session_state.vector_store = build_collection(texts, DB_PATH)
                st.session_state.repo_indexed = True
                st.success("✅ Repository indexed!")
        else:
            st.error("Enter link git!!! Fk you if you do something weird")


st.caption("Chat with Gemini 3 Flash Preview")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about code in this repo..."):
    if not st.session_state.repo_indexed:
        st.warning("You haven't enter repository!")
    else:

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            with st.spinner("Reading code ..."):

                answer = answer_question(prompt, st.session_state.vector_store)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})