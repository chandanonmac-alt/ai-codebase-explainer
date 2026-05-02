class UserService:

    def __init__(self, user_repo):
        self.user_repo = user_repo

    def create_user(self, user_id):
        return self.user_repo.save({"user_id": user_id})