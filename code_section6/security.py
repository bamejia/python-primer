from hmac import compare_digest
from code_section6.models.usermodel import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):  # payload is contents of JWT token
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)