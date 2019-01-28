import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from appfactory import db


class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	messages = db.relationship('Message', backref='user', lazy=True)

	def record_message(self, message):
		message = Message(message=message, user_id=self.id, channel_id=channels.id)
		db.session.add(message)
		db.session.commit()


class Channel(db.Model):

	__tablename__ = 'channels'

	id = db.Column(db.Integer, primary_key=True)
	channel = db.Column(db.String, unique=True, nullable=False)
	messages = db.relationship("Message", backref="channel", lazy=True)


class Message(db.Model):

	__tablename__ = 'messages'

	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)

