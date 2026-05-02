import pickle
from code_loader import load_code_files
from embeddings import create_embedding
from vector_store import VectorStore


# 🔥 Chunking (line-based)
def chunk_code(text, max_lines=30):
    lines = text.split("\n")
    chunks = []

    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i:i + max_lines])
        chunks.append(chunk)

    return chunks


# 🔥 Layer detection based on folder structure
def get_category(filepath):
    path = filepath.lower()

    if "controllers" in path:
        return "controller layer"
    elif "services" in path:
        return "service layer"
    elif "repository" in path:
        return "data access layer"
    elif "models" in path:
        return "data model"
    elif "utils" in path:
        return "utility"
    elif "config" in path:
        return "configuration"
    else:
        return "miscellaneous"


# 🔥 MAIN
folder = "./ai-productivity-assistant"

files = load_code_files(folder)

store = VectorStore()

print("Indexing structured codebase...\n")


# 🔥 Enhanced repo summary
summary_text = """
REPO_SUMMARY

This is a layered backend system with the following architecture:

- Controller layer (handles incoming requests)
- Service layer (business logic)
- Repository layer (data access)
- Models (data structures)
- Utility modules (helpers, logging, validation)
- Configuration management

Files:
"""

for file in files:
    summary_text += f"- {file['filepath']}\n"

embedding = create_embedding(summary_text)
store.add(embedding, summary_text)


# 🔥 INGESTION LOOP
for file in files:

    filepath = file["filepath"]
    content = file["content"]

    chunks = chunk_code(content, max_lines=30)

    # 🔥 Limit chunks per file
    MAX_CHUNKS_PER_FILE = 5
    limited_chunks = chunks[:MAX_CHUNKS_PER_FILE]

    for chunk in limited_chunks:

        category = get_category(filepath)

        text_with_metadata = f"""
FILE: {filepath}
CATEGORY: {category}

{chunk}
"""

        embedding = create_embedding(text_with_metadata)
        store.add(embedding, text_with_metadata)


print("\nIndexing complete.")

# Save DB
with open("vector_store.pkl", "wb") as f:
    pickle.dump(store, f)

print("Vector database saved.")