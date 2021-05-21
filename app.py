from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os

from code_section6.security import authenticate, identity
from code_section6.resources.user_resource import UserRegister
from code_section6.resources.item_resource import ItemDAO, ItemListDAO
from code_section6.resources.store_resource import StoreListResource, StoreResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Tom"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemDAO, "/item/<string:name>")
api.add_resource(ItemListDAO, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreListResource, "/stores")


if __name__ == "__main__":
# def run():
    from code_section6.db import db
    db.init_app(app)
    # app.run(port=5000, debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

