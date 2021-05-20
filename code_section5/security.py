from hmac import compare_digest
from user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):  # payload is contents of JWT token
    user_id = payload["identity"]
    return User.find_by_id(user_id)