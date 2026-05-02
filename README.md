# 🧠 AI Codebase Explainer (RAG)

A Retrieval-Augmented Generation (RAG) based application that analyzes and explains codebases using semantic search and a local LLM.

---

## 🚀 Overview

Understanding unfamiliar codebases can be time-consuming. This project solves that by combining:

- **Semantic code search** using embeddings
- **Context-aware reasoning** using an LLM
- **Structured prompt engineering** to reduce hallucination

👉 Ask questions about any codebase and get clear, contextual explanations.

---

## ✨ Key Features

- 🔍 **Semantic Retrieval**  
  Finds relevant code snippets using embeddings (not keyword search)

- 🧠 **Context-Aware Explanations**  
  Generates answers grounded in retrieved code context

- ⚡ **Reranking for Better Precision**  
  Improves relevance by filtering top results

- 🧱 **Structured Prompting**  
  Ensures consistent and logical responses

- 🛑 **Hallucination Control**  
  Encourages evidence-based answers (e.g., “no evidence found”)

---

## 🏗️ Architecture
User Query
↓
Embedding Generation
↓
Vector Search (FAISS)
↓
Top-K Retrieval + Reranking
↓
Context Construction
↓
LLM (Ollama)
↓
Final Answer

---

## 🧰 Tech Stack

- **Language:** Python  
- **Embeddings:** sentence-transformers  
- **Vector Store:** FAISS  
- **LLM:** Ollama (local)  
- **UI:** Streamlit  

---

## 📂 Project Structure

├── ai-productivity-assistant # Sample Repo to try out this application with
├── app.py # Streamlit UI
├── ingest.py # Codebase ingestion + chunking
├── query.py # Retrieval + response generation
├── vector_store.py # Backend logic for Vector_store
├── embeddings.py # Embedding generation
├── code_loader.py # Loads codebase from sample repo , replace repo name here if needed.
├── requirements.txt
└── README.md


---

## ⚙️ How It Works

### 1. Ingestion Phase
- Reads code files
- Splits them into chunks
- Generates embeddings
- Stores them in a FAISS index

### 2. Query Phase
- Converts user question into embedding
- Retrieves relevant code chunks
- Applies reranking and filtering
- Sends structured context to LLM

### 3. Response Generation
- LLM generates explanation grounded in retrieved context

---

## ▶️ How to Run

### 1. Clone the repository
git clone <this-repo-url>
cd ai-code-explainer-advanced

---

### 2. Install dependencies
pip install -r requirements.txt

---

### 3. Run ingestion
python ingest.py

---

### 4. Start the app
streamlit run app.py


---

## 💡 Sample Questions

Try asking:

- What are the main modules in this project?
- Which files handle data access?
- Which function interacts with the repository?
- Does this project use caching?
- Is there any authentication mechanism?

---

## 🧪 What This Project Demonstrates

- End-to-end **RAG pipeline implementation**
- Improved retrieval using **reranking**
- **Structured prompt engineering**
- Handling **edge cases & negative queries**
- Reducing **LLM hallucination**

---

## 📌 Key Learnings

- Retrieval quality directly impacts answer quality  
- Structured context improves consistency  
- Prompt design controls reasoning behavior  
- Negative testing is critical for robustness  

---

## 🚀 Future Improvements

- Query intent routing  
- Function-level chunking  
- Dependency awareness  
- Multi-query retrieval  
- Stateful memory  

---

## 🤝 Contributions

This is a personal learning project. Feedback and suggestions are welcome!

---

## 📬 Connect

If you're working on RAG systems or AI engineering, feel free to connect and discuss ideas.