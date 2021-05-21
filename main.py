from app import app
from code_section6.db import db


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)