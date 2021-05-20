from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from contextlib import closing
import sqlite3
import sys


class Item:
    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price


class ItemDAO(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        with closing(sqlite3.connect("data.db")) as connection, \
                closing(connection.cursor()) as cursor:
            select_query = "SELECT * from Items where name=?"
            result = cursor.execute(select_query, (name,)).fetchone()
            if result:
                item = Item(*result).__dict__
            else:
                item = None

            connection.commit()

        return item

    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists"}, 400

        try:
            is_inserted = self.insert(name)
        except sqlite3.DatabaseError as e:
            print(e, file=sys.stderr)
            return {"message": "An error occurred when inserting the item"}, 500
        if is_inserted:
            return {"message": f"Item '{name}' has been successfully added."}, 201
        return {"message": f"Item '{name}' could not be added."}, 500

    @classmethod
    def insert(cls, name):
        data = cls.parser.parse_args()

        with closing(sqlite3.connect("data.db")) as connection, \
                closing(connection.cursor()) as cursor:
            insert_query = "INSERT INTO ITEMS VALUES(NULL,?,?)"
            cursor.execute(insert_query, (name, data["price"]))
            connection.commit()
            if cursor.rowcount:
                return True
            return False

    def delete(self, name):
        with closing(sqlite3.connect("data.db")) as connection, \
                closing(connection.cursor()) as cursor:
            delete_query = "DELETE from Items where name=?"
            cursor.execute(delete_query, (name,))
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": f"Item '{name}' deleted successfully."}, 201
            return {"message": f"Item '{name}' could not be deleted"}, 400

    def put(self, name):
        item = self.find_by_name(name)
        data = self.parser.parse_args()

        with closing(sqlite3.connect("data.db")) as connection, \
                closing(connection.cursor()) as cursor:
            if item:
                update_query = "UPDATE items set price=? where name=?"
                cursor.execute(update_query, (data["price"], name))
                connection.commit()
                return {"message": f"Item '{name}' has been successfully updated."}, 200
            else:
                try:
                    is_inserted = self.insert(name)
                except sqlite3.DatabaseError as e:
                    print(e, file=sys.stderr)
                    return {"message": "An error occurred when inserting the item"}, 500

                if is_inserted:
                    return {"message": f"Item '{name}' has been successfully added."},
                return {"message": f"Item '{name}' could not be added."}, 500


class ItemListDAO(Resource):
    # @jwt_required()
    def get(self):
        with closing(sqlite3.connect("data.db")) as connection, \
                closing(connection.cursor()) as cursor:
            select_query = "SELECT * from Items"
            result = cursor.execute(select_query).fetchall()
            items = [Item(*item).__dict__ for item in result]

            connection.commit()

        return {"items": items}
