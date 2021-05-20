import sqlite3
from flask_restful import Resource, reqparse
from models.usermodel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("password", type=str, required=True, help="This field cannot be left blank")

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": f"User '{data['username']}' already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": f"User '{user.username}' has been successfully created"}, 201

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(insert_query, (user["username"], user["password"]))
        #
        # connection.commit()
        # connection.close()
        #
        # return {"message": f"User '{user['username']}' has been successfully created"}, 201

