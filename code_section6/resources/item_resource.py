from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy.exc import DatabaseError
from contextlib import closing
import sqlite3
import sys

from code_section6.models.itemmodel import ItemModel


class ItemDAO(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists"}, 400

        data = self.parser.parse_args()
        try:
            item = ItemModel(name, **data)
            is_inserted = item.save_to_db()
        except DatabaseError as e:
            print(e, file=sys.stderr)
            return {"message": "An error occurred when inserting the item"}, 500

        if is_inserted:
            return {"message": f"Item '{name}' has been successfully added."}, 201
        return {"message": f"Item '{name}' could not be added."}, 500

    def delete(self, name):
        # with closing(sqlite3.connect("data.db")) as connection, \
        #         closing(connection.cursor()) as cursor:
        #     delete_query = "DELETE from Items where name=?"
        #     cursor.execute(delete_query, (name,))
        #     connection.commit()
        #
        #     if cursor.rowcount > 0:
        #         return {"message": f"Item '{name}' deleted successfully."}, 201
        #     return {"message": f"Item '{name}' could not be deleted"}, 400
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {"message": f"Item '{name}' deleted successfully."}, 201
        else:
            return {"message": f"Item '{name}' does not exist"}, 404

    def put(self, name):
        item = ItemModel.find_by_name(name)
        data = self.parser.parse_args()

        if item:
            item.price = data["price"]
            item.store_id = data["store_id"]
            try:
                is_updated = item.save_to_db()
            except DatabaseError as e:
                print(e)
                return {"message": "An error occurred when inserting the item"}, 500
            if is_updated:
                return {"message": f"Item '{name}' has been successfully updated."}, 200
            return {"message": f"Item '{name}' could not be updated."}, 500
        else:
            try:
                item = ItemModel(name, **data)
                is_inserted = item.save_to_db()
            except DatabaseError as e:
                print(e, file=sys.stderr)
                return {"message": "An error occurred when inserting the item"}, 500

            if is_inserted:
                return {"message": f"Item '{name}' has been successfully added."}, 201
            return {"message": f"Item '{name}' could not be added."}, 500


class ItemListDAO(Resource):
    # @jwt_required()
    def get(self):
        items = ItemModel.get_all_items()
        return {"items": [item.json() for item in items]}, 200
        # with closing(sqlite3.connect("data.db")) as connection, \
        #         closing(connection.cursor()) as cursor:
        #     select_query = "SELECT * from Items"
        #     result = cursor.execute(select_query).fetchall()
        #     items = [ItemModel(*item).__dict__ for item in result]
        #
        #     connection.commit()
        #
        # return {"items": items}
