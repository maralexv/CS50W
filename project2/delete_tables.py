from init import app, db
from models import *

db.init_app(app)

def delete():
    db.drop_all()

if __name__ == "__main__":
    with app.app_context():
        delete()