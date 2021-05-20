from hmac import compare_digest
from user import User

users = [
    User(1, "Bob", "asdf")
]

username_mapping = {user.username: user for user in users}
userid_mapping = {user.id: user for user in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user


def identity(payload):  # payload is contents of JWT token
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)