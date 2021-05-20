from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import ItemDAO, ItemListDAO

app = Flask(__name__)
app.secret_key = "Tom"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemDAO, "/item/<string:name>")
api.add_resource(ItemListDAO, "/items")
api.add_resource(UserRegister, "/register")
app.run(port=11111, debug=True)
