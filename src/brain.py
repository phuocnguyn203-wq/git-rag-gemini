from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
api_key = os.environ.get("GOOGLE_API_KEY", " ")
MODEL = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0, api_key=api_key)


def answer_question(question, vector_store, llm=MODEL, k=15):
    system_prompt = (
        "You are a Senior Engineer. Use the provided code to answer the question. "
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
    response = rag_chain.invoke({"input": question})
    return response["answer"]
