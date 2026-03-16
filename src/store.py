from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

def create_texts(docs):
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, 
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = python_splitter.split_documents(docs)
    print(f"Created {len(texts)} chunks from code.")
    return texts

llm = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
def build_collection(texts, db_path):
    if os.path.exists(db_path):
        vector_store = Chroma(
            persist_directory=db_path,
            embedding_function=llm,
            collection_name="repo"
        )
        vector_store.add_documents(texts)
        print(f"Added {len(texts)} code snippets to the collection.")
    else:
        vector_store = Chroma.from_documents(
            documents=texts,
            embedding=llm,
            persist_directory=db_path,
            collection_name="repo"
        )
        print(f"Success! Indexed {vector_store._collection.count()} code snippets.")
    print(f"Total documents: {vector_store._collection.count()}")
    return vector_store
