from flask_login import UserMixin
import json

with open('user_roles.json') as user_roles:
    USER_ROLES = json.load(user_roles)
    
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def has_writer_role(self):
        return USER_ROLES.get(self.id) == 'writer'
    


