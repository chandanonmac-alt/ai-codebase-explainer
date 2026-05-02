class UserRepository:

    def __init__(self):
        self.users = []

    def save(self, user):
        self.users.append(user)
        return user