from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    # self.* must match these to be put into table by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {"id": self.id, "username": self.username, "password": self.password}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * from users where username=?"
        # cursor.execute(query, (username,))
        # row = cursor.fetchone()
        # if row:
        #     user = cls(*row)  # row[0], row[1], row[2]
        # else:
        #     user = None
        # connection.close()
        #
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * from users where id=?"
        # cursor.execute(query, (_id,))
        # row = cursor.fetchone()
        # if row:
        #     user = cls(*row)  # row[0], row[1], row[2]
        # else:
        #     user = None
        # connection.close()
        #
        # return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return True

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return True