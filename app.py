import streamlit as st
import pickle
import requests
from embeddings import create_embedding

st.title("AI Codebase Explainer")

# Load vector store
with open("vector_store.pkl", "rb") as f:
    store = pickle.load(f)

question = st.text_input("Ask a question about the codebase")

if question:

    # 1️⃣ Create embedding
    question_embedding = create_embedding(question)

    # 2️⃣ Retrieve more results
    results = store.search(question_embedding, k=20)

    # 3️⃣ Deduplicate (1 chunk per file)
    unique_results = []
    seen_files = set()

    for chunk in results:
        lines = chunk.split("\n")

        filename = None
        for line in lines:
            if "FILE:" in line:
                filename = line.replace("FILE:", "").strip()
                break

        if filename and filename not in seen_files:
            seen_files.add(filename)
            unique_results.append(chunk)

    # 4️⃣ Add diversity (hybrid retrieval)
    import random
    all_chunks = store.text_chunks.copy()
    random.shuffle(all_chunks)

    for chunk in all_chunks:
        lines = chunk.split("\n")

        filename = None
        for line in lines:
            if "FILE:" in line:
                filename = line.replace("FILE:", "").strip()
                break

        if filename and filename not in seen_files:
            seen_files.add(filename)
            unique_results.append(chunk)

        if len(unique_results) >= 6:
            break

    # 5️⃣ Add repo summary
    summary_chunks = [c for c in store.text_chunks if "REPO_SUMMARY" in c]

    # 6️⃣ Final context
    context = "\n\n".join(summary_chunks + unique_results)

    # 7️⃣ Debug view (hidden)
    with st.expander("🔍 Retrieved Context (Debug Only)"):
        st.code(context)

    # 8️⃣ Call LLM
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": f"""
You are a senior software engineer.

Analyze the provided codebase context and answer the question.

IMPORTANT:
- Summarize at a high level
- Group similar functionality
- Use FILE and CATEGORY info

Context:
{context}

Question:
{question}

Answer:
""",
            "stream": False
        }
    )

    answer = response.json()["response"]

    # 9️⃣ Show answer
    st.subheader("Explanation")
    st.write(answer)