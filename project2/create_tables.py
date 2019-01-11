import app, db
from models import *

db.init_app(app)

def create():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        create()