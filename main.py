from app import app
from code_section6.db import db
from os import environ


db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# app.run(host='0.0.0.0', debug=False, port=environ.get("PORT", 11111))