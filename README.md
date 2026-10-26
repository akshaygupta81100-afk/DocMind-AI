# DocMind — AI-Powered PDF Assistant

DocMind is an AI-powered PDF assistant that allows users to upload PDF documents, ask questions about their content, and receive relevant answers with source page references. It combines document processing, intelligent text retrieval, and Large Language Models (LLMs) to make reading and understanding documents faster and easier.

## 🚀 Features

- **PDF Upload & Processing:** Upload PDF documents and extract their text for analysis.
- **Ask Questions About Your Documents:** Ask natural-language questions and get context-aware answers.
- **AI-Powered Responses:** Uses the Groq API with an LLM to generate answers based on document content.
- **Smart Text Retrieval:** Uses TF-IDF vectorization and cosine similarity to identify relevant sections of a document.
- **Source Page References:** Helps users locate the pages supporting the retrieved information.
- **Interactive Web Interface:** A simple interface built with Streamlit.
- **Conversation History:** Keeps the current session's question-and-answer history available while using the application.
- **Modular Project Structure:** Includes backend and frontend folders for organizing the application components.

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — Web application interface
- **PyMuPDF** — PDF text extraction
- **Scikit-learn** — TF-IDF and cosine similarity
- **Groq API** — AI-powered answer generation
- **Requests** — API communication

## ⚙️ How It Works

1. Upload a PDF document.
2. DocMind extracts text from the PDF.
3. The retrieval system identifies relevant text sections based on the user's question.
4. The relevant context is sent to the language model through the Groq API.
5. The application displays the generated answer and relevant source page references.

## 💻 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/akshaygupta81100-afk/DocMind.git
cd DocMind
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.streamlit/secrets.toml` file and add your Groq API key:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Keep your API key private. Do not commit your secrets file to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in your terminal to use DocMind.

## 🌐 Live Demo

Try DocMind online:

[**Launch DocMind**](https://docmind-mzdx3lsnjizrxf7tftcwyp.streamlit.app/)

## 🎯 Project Goal

The goal of DocMind is to simplify document analysis by helping students, researchers, and professionals find relevant information in PDF files without manually searching through every page.

## 🔮 Future Improvements

- Support for multiple PDF documents
- Persistent chat history
- More advanced semantic search and retrieval
- Improved answer citations and source highlighting
- Enhanced user interface and document management
- Support for additional document formats

## 🔐 Security Note

API credentials should be stored securely using Streamlit secrets or environment variables. Never publish private API keys in source code or public repositories.

## 👨‍💻 Author

**Akshay Gupta**

Built with Python, AI, and a focus on making document understanding simpler.
