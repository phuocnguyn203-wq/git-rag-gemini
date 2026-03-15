# 🚀 AI Code RAG Explorer (AI generated readme)

**AI Code RAG Explorer** is an open-source tool that allows you to "chat" directly with any Python codebase repository on GitHub. 

Instead of manually reading thousands of lines of code, simply provide a GitHub link. The system will automatically fetch the source code, parse it, and use **RAG (Retrieval-Augmented Generation)** combined with the **Gemini 3 Flash** model to answer any questions you have about that project.

## ✨ Key Features

- **Fully Automated (Plug & Play):** Just enter a GitHub link, and the system handles `git clone`, code splitting (chunking), and vector storage automatically.
- **Semantic Search:** Utilizes the `BAAI/bge-small-en-v1.5` embedding model to find the most relevant code snippets based on meaning, not just exact keyword matches.
- **Deep Code Understanding:** Leverages the power of the **Gemini 3 Flash** model to analyze logic, architecture, and explain complex source code.
- **User-Friendly Interface:** Easy and interactive chat experience through a Web UI built with **Streamlit**.

## 🛠️ Prerequisites

- **Python:** 3.10+
- **Git:** Installed on your local machine.
- **API Key:** A valid Google API Key (obtainable for free at [Google AI Studio](https://aistudio.google.com/)).

## 🚀 Installation Guide

**1. Clone the repository:**
```bash
git clone https://github.com/phuocnguyen-hask/code_rag.git
cd code_rag
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables:**
Create a file named `.env` in the root directory (alongside `requirements.txt`) and add your Google API Key:
```env
GOOGLE_API_KEY=your_api_key_here
```

## 💻 Usage

To launch the Web UI, run the following command in your terminal:

```bash
streamlit run src/app.py
```

1. Open your browser and navigate to `http://localhost:8501`.
2. Paste the GitHub link of the Python project you want to analyze into the left sidebar (e.g., `https://github.com/pallets/flask.git`).
3. Click **Index Repository** and wait for the system to ingest the codebase.
4. Start chatting and asking questions in the main chat window!

## 📂 Project Structure

```text
code_rag/
├── data/               # Temporary folder for cloned source code (Auto-generated)
├── db/                 # Folder containing the ChromaDB Vector Store (Auto-generated)
├── src/                # Main application source code
│   ├── app.py          # Streamlit UI
│   ├── brain.py        # RAG Engine logic & Gemini configuration
│   ├── loader.py       # Git clone logic & Document Loader
│   └── store.py        # Text Splitting & Vector Database logic
├── .env                # Environment variables (Contains API Key)
└── requirements.txt    # List of required dependencies
```

## 🤖 About this Document

> **Note:** The project structure and this README were drafted and optimized by **Gemini**, an AI assistant, to support the packaging and release of this Open Source project in a standard and professional manner. The core source code was developed and is maintained by a human engineer.
