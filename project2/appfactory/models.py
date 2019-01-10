from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from appfactory import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


