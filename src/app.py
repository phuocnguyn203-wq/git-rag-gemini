import streamlit as st
from pathlib import Path

from loader import load_repo, clone_repo
from store import create_texts, build_collection
from brain import answer_question


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.mkdir(parents=True, exist_ok=True)


def get_data_path(index: int) -> Path:
    return DATA_DIR / f"repo{index}"


st.set_page_config(page_title="Code RAG Explorer", page_icon="💻")
st.title("🚀 AI Code RAG Explorer")
st.caption("Chat with Gemini 3 Flash Preview")


if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "repo_indexed" not in st.session_state:
    st.session_state.repo_indexed = False

if "current_index" not in st.session_state:
    st.session_state.current_index = 0


with st.sidebar:
    st.header("Repository Settings")

    git_link = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/user/repo"
    )

    if st.button("Index Repository"):

        if not git_link:
            st.error("Please enter a GitHub repository URL.")
        else:

            with st.spinner("Indexing repository..."):

                repo_index = st.session_state.current_index
                folder_path = get_data_path(repo_index)

                clone_repo(git_link, folder_path)

                docs = load_repo(folder_path)

                texts = create_texts(docs)

                st.session_state.vector_store = build_collection(
                    texts,
                    DB_PATH
                )

                st.session_state.repo_indexed = True
                st.session_state.current_index += 1

                st.success("✅ Repository indexed successfully!")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask me about the code in this repository...")

if prompt:

    if not st.session_state.repo_indexed:
        st.warning("⚠️ Please index a repository first.")
    else:

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Reading code..."):

                answer = answer_question(
                    prompt,
                    st.session_state.vector_store
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )