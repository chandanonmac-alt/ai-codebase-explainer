from app.routes import create_task, get_tasks

if __name__ == "__main__":
    print("AI Productivity Assistant Backend Running...")
    
    # Demo run
    create_task("user1", "Learn RAG deeply")
    tasks = get_tasks("user1")
    print(tasks)