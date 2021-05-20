from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_resource import UserRegister
from resources.item_resource import ItemDAO, ItemListDAO
from resources.store_resource import StoreListResource, StoreResource
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Tom"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(ItemDAO, "/item/<string:name>")
api.add_resource(ItemListDAO, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreListResource, "/stores")


if __name__ == "__main__":
    # def run():
    db.init_app(app)
    app.run(port=11111, debug=True)
