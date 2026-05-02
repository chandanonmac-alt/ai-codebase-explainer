import os

def load_code_files(root_dir):
    """
    Recursively load all Python files from a project.
    Returns list of dicts with filename, path, and content.
    """

    code_files = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    relative_path = os.path.relpath(full_path, root_dir)

                    code_files.append({
                        "filename": file,
                        "filepath": relative_path,   # 🔥 NEW (important)
                        "content": content
                    })

                except Exception as e:
                    print(f"Skipping {full_path}: {e}")

    return code_files