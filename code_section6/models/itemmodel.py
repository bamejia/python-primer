# import sqlite3
# from contextlib import closing
from code_section6.db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"id": self.id, "name": self.name, "price": self.price, "store_id": self.store_id}

    @classmethod
    def find_by_name(cls, name):
        # with closing(sqlite3.connect("data.db")) as connection, \
        #         closing(connection.cursor()) as cursor:
        #     select_query = "SELECT * from Items where name=?"
        #     result = cursor.execute(select_query, (name,)).fetchone()
        #     if result:
        #         item = cls(*result)
        #     else:
        #         item = None
        #     connection.commit()
        #
        # return item
        return cls.query.filter_by(name=name).first()  # Select * from items where name = name LIMIT 1
                                                # filter_by(name=name).filter_by(id=id) == filter_by(name=name, id=id)

    # def insert(self):
        # with closing(sqlite3.connect("data.db")) as connection, \
        #         closing(connection.cursor()) as cursor:
        #     insert_query = "INSERT INTO ITEMS VALUES(NULL,?,?)"
        #     cursor.execute(insert_query, (self.name, self.price))
        #     connection.commit()
        #     if cursor.rowcount:
        #         return True
        #     return False
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return True

    # def update(self):
    #     with closing(sqlite3.connect("data.db")) as connection, \
    #             closing(connection.cursor()) as cursor:
    #
    #         update_query = "UPDATE items set price=? where name=?"
    #         cursor.execute(update_query, (self.price, self.name))
    #         connection.commit()
    #         return True

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return True

    @classmethod
    def get_all_items(cls):
        return cls.query.all()
