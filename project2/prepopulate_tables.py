# import time
import random
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from appfactory import app, db
from appfactory.models import *

db.init_app(app)

def prepopulate():
	''' pre-populate db tables (if they are empty) for tests'''

	# fetch all the data from db tables
	users = User.query.all() 
	channels = Channel.query.all()
	messages = Message.query.all()

	# add users
	if users == []:
		for user_n in range(1,4):
			user = User(name=(f"User-{user_n}"))
			db.session.add(user)
			db.session.commit()

	# add channels
	if channels == []:
		for channel_n in range (1,8):
			channel = Channel(channel=(f"Channel Number {channel_n}"))
			db.session.add(channel)
			db.session.commit()

	# add messages
	texts = ['Hello World!', 'Oh! what a day!', 'Not for me.', 'Seriously?', 'Hi there...']
	if messages == []:
		for mes_n in range(1, 51):
			text = texts[random.randint(0,4)]
			message = Message(message=(f"Phrase {mes_n}: {text}"), user_id = random.randint(1,3), channel_id = random.randint(1,7))
			db.session.add(message)
			db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        prepopulate()