from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "Tom"
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


# class Student(Resource):
#     def get(self, name):
#         return {"student": name}


# api.add_resource(Student, "/student/<string:name>")
# app.run(port=11111)

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda i: i["name"] == name, items), None):
            return {"message": f"An item with name '{name}' already exists"}, 400

        # request_body = request.get_json()  # can pass silent=True for no error and just returns None, or can pass
        # force=True and makes request a json without looking at http header

        request_body = Item.parser.parse_args()
        price = request_body["price"]
        item = {"name": name, "price": price}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda i: i["name"] != name, items))
        return {"message": "item deleted"}, 200

    def put(self, name):
        item = next(filter(lambda i: i["name"] == name, items), None)
        request_body = Item.parser.parse_args()
        price = request_body["price"]

        if item:
            item.update(request_body)
            # item["price"] = price
            # items.append(item)
            return item, 200
        else:
            item = {"name": name, "price": price}
            items.append(item)
            return item, 201


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
app.run(host="192.168.1.173", port=11111, debug=True)
