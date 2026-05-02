import pickle
import requests
import random
import re
from collections import defaultdict
from embeddings import create_embedding
from sentence_transformers import CrossEncoder

print("Starting query engine...")

# Load vector store
with open("vector_store.pkl", "rb") as f:
    store = pickle.load(f)

print("Vector store loaded.")

# 🔥 Initialize reranker
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')


# ==============================
# 🔥 Multi-query generation
# ==============================
def generate_queries(question):
    return [
        question,
        f"Explain {question}",
        f"In simple terms, {question}",
        f"Detailed explanation of {question}"
    ]


# ==============================
# 🔥 Extract function names
# ==============================
def extract_functions(chunk):
    return re.findall(r"def\s+(\w+)\(", chunk)


# ==============================
# 🔥 Group chunks by file
# ==============================
def group_by_file(chunks):
    file_map = defaultdict(list)

    for chunk in chunks:
        lines = chunk.split("\n")

        filepath = None
        for line in lines:
            if "FILE:" in line:
                filepath = line.replace("FILE:", "").strip()
                break

        if filepath:
            file_map[filepath].append(chunk)

    return file_map


# ==============================
# 🔥 Build structured context
# ==============================
def build_structured_context(file_map):

    context_parts = []

    for filepath, chunks in file_map.items():

        # Extract unique functions
        functions = []
        for chunk in chunks:
            functions.extend(extract_functions(chunk))

        functions = list(set(functions))

        section = f"\nFILE: {filepath}\n"

        if functions:
            section += "FUNCTIONS:\n"
            for fn in functions:
                section += f"- {fn}\n"

        section += "\nCODE:\n"
        section += "\n\n".join(chunks[:2])  # limit chunks per file

        context_parts.append(section)

    return "\n\n".join(context_parts)


# ==============================
# 🔥 MAIN LOOP
# ==============================
while True:

    question = input("\nAsk about the codebase (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    # ==============================
    # 1️⃣ Multi-query retrieval
    # ==============================
    all_results = []
    queries = generate_queries(question)

    for q in queries:
        q_embedding = create_embedding(q)
        results = store.search(q_embedding, k=20)
        all_results.extend(results)

    # ==============================
    # 2️⃣ Deduplicate chunks
    # ==============================
    unique_chunks = list(set(all_results))

    # ==============================
    # 3️⃣ Reranking
    # ==============================
    pairs = [(question, chunk) for chunk in unique_chunks]
    scores = reranker.predict(pairs)

    ranked_results = sorted(
        zip(unique_chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Top chunks
    top_chunks = [r[0] for r in ranked_results[:6]]

    # ==============================
    # 4️⃣ File-level deduplication
    # ==============================
    unique_results = []
    seen_paths = set()

    for chunk in top_chunks:
        lines = chunk.split("\n")

        filepath = None
        for line in lines:
            if "FILE:" in line:
                filepath = line.replace("FILE:", "").strip()
                break

        if filepath and filepath not in seen_paths:
            seen_paths.add(filepath)
            unique_results.append(chunk)

    # ==============================
    # 5️⃣ Hybrid fallback (optional diversity)
    # ==============================
    all_chunks = store.text_chunks.copy()
    random.shuffle(all_chunks)

    for chunk in all_chunks:
        lines = chunk.split("\n")

        filepath = None
        for line in lines:
            if "FILE:" in line:
                filepath = line.replace("FILE:", "").strip()
                break

        if filepath and filepath not in seen_paths:
            seen_paths.add(filepath)
            unique_results.append(chunk)

        if len(unique_results) >= 6:
            break

    # ==============================
    # 6️⃣ Add repo summary
    # ==============================
    summary_chunks = [
        c for c in store.text_chunks if "REPO_SUMMARY" in c
    ]

    # ==============================
    # 7️⃣ 🔥 STRUCTURED CONTEXT
    # ==============================
    file_map = group_by_file(unique_results)
    structured_context = build_structured_context(file_map)

    context = "\n\n".join(summary_chunks) + "\n\n" + structured_context

    # ==============================
    # 🔍 Debug: Files used
    # ==============================
    print("\nFILES USED IN CONTEXT:")
    for f in file_map.keys():
        print(f"FILE: {f}")

    # ==============================
    # 8️⃣ LLM CALL
    # ==============================
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": f"""
You are a senior software engineer.

STRICT RULES:
- ONLY use information explicitly present in the context
- DO NOT assume or infer missing files
- DO NOT create extra categories like "miscellaneous"
- Focus only on core architectural layers
- Always include a "Flow" section explaining how layers interact end-to-end
- Answer ONLY what is asked
- Do NOT include indirect interactions unless explicitly asked
- Prefer direct function-to-repository interactions
- Avoid adding explanations beyond scope
- Identify ONLY direct interactions (function → repository call)
- Do NOT include indirect calls via other layers
- Do NOT include repository functions themselves unless explicitly asked
- Keep the answer focused and minimal
- For questions about system capabilities, first check if evidence exists
- If not, clearly say “no evidence found”
- Avoid giving unrelated context or summaries
- Keep answers concise and focused on the question
- Answer the question directly first
- Avoid giving unrelated summaries or file listings
- Keep answers concise and focused

TASK:
1. Identify the architectural layers present in the system
2. For each layer, list the actual files from the context
3. Briefly explain the role of each layer
4. MUST include a clear flow showing how layers interact

OUTPUT FORMAT:
- Use clean sections for each layer
- End with a "Flow" section explaining interactions

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

    # ==============================
    # 9️⃣ OUTPUT
    # ==============================
    print("\nAI Explanation:\n")
    print(answer)