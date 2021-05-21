from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from os import environ

from code_section6.security import authenticate, identity
from code_section6.resources.user_resource import UserRegister
from code_section6.resources.item_resource import ItemDAO, ItemListDAO
from code_section6.resources.store_resource import StoreListResource, StoreResource
from code_section6.resources.home_resource import Home

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL2', 'sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Tom"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemDAO, "/item/<string:name>")
api.add_resource(ItemListDAO, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreListResource, "/stores")
api.add_resource(Home, "/")


if __name__ == "__main__":
    from code_section6.db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(host='0.0.0.0', debug=True, port=environ.get("PORT", 11111))


