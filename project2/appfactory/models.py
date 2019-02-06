import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from appfactory import db


class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)


	def users_list():
		''' returns a list of the names of all users '''
		us = User.query.all()
		return [i.name for i in us]


	def all_users():
		return User.query.all()


	def add_user(name):
		user = User(name=name)
		db.session.add(user)
		db.session.commit()



class Channel(db.Model):

	__tablename__ = 'channels'

	id = db.Column(db.Integer, primary_key=True)
	channel = db.Column(db.String, unique=True, nullable=False)


	def channels_list():
		''' returns a list of titles of all channels '''
		ch = Channel.query.all()
		return [i.channel for i in ch]


	def add_channel(chat):
		channel = Channel(channel=chat)
		db.session.add(channel)
		db.session.commit()



class Message(db.Model):

	__tablename__ = 'messages'

	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)


	def add_mes(text, userid, channelid):
		mes = Message(message=text, user_id=userid, channel_id=channelid)
		db.session.add(mes)
		db.session.commit()


	def channels_by_user(userid):
		''' returns unorderd list of channle IDs of soecific user '''
		messages = Message.query.filter_by(user_id=userid).all()
		channel_id_list = []
		for i in messages:
			if i.channel_id not in channel_id_list:
				channel_id_list.append(i.channel_id)
		return channel_id_list


	def messages_by_channel(channelid):
		''' returns list of objects, each of which has Message data, accessible with '.' 
		e.g. messages_by_channel[0].date_time would return timestamp for the 1st message in list,
		messages_by_channel[1].message would return the text of the message for the 2nd message 
		in list, etc.
		'''
		return Message.query.filter_by(channel_id=channelid).all()

