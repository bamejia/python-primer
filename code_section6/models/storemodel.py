# import sqlite3
# from contextlib import closing
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic")  # lazy="dynamic" makes items a query builder

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name, "items": [item.json() for item in self.items.all()]}  # .all gets list from query

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # Select * from items where name = name LIMIT 1
                                                # filter_by(name=name).filter_by(id=id) == filter_by(name=name, id=id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return True

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @classmethod
    def get_all_stores(cls):
        return cls.query.all()
