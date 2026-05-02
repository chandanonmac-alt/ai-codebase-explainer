import json

class TaskRepository:

    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, task):
        data = self._read()
        data.append(task)
        self._write(data)
        return task

    def find_by_user(self, user_id):
        data = self._read()
        return [t for t in data if t["user_id"] == user_id]

    def _read(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except:
            return []

    def _write(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f)