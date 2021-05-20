from flask_restful import Resource
from models.storemodel import StoreModel
from sqlalchemy.exc import DatabaseError
import sys


class StoreResource(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": f"Store '{name}' does not exist"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"Store '{name}' already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except DatabaseError as e:
            print(e, file=sys.stderr)
            return {"message": f"An error occurred when attempting to add store '{name}'"}, 500
        return {"message": f"Store '{name}' has been successfully created"}, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
                return {"message": f"Store '{name}' has been successfully deleted"}, 201
            except DatabaseError as e:
                print(e, file=sys.stderr)
                return {"message": f"An error occurred when attempting to delete store '{name}'"}, 500
        else:
            return {"message": f"Store '{name}' does not exist"}, 404


class StoreListResource(Resource):
    def get(self):
        stores = StoreModel.get_all_stores()
        return {"stores": [store.json() for store in stores]}, 200
