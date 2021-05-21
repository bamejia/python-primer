from code_section6.app import app
from code_section6.db import db


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    db.init_app(app)