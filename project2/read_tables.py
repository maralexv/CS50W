from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from appfactory import app, db
from appfactory.models import *

db.init_app(app)

def read():
	''' read and report back from db tables '''

	# fetch all the users
	print(User.query.all())
	users = User.users_list() 
	print('\nAll Users:')
	print(users)
	username = 'User-2'
	user = User.query.filter_by(name=username).first()
	print (type(user))
	print(f"{user.name}'s ID is {user.id}")


	# fetch all the chat channels
	channels = Channel.channels_list()
	print('\nAll Chat Channels:')
	print(channels)
	print(type(channels))

	# fetch messages of specific user
	u = 3
	channels = Message.channels_by_user(u)
	channelsnames = []
	for i in channels:
		channelsnames.append(Channel.query.get(i).channel)
	print(f'\nAll Chat Channels for User {u}')
	print(channelsnames)

	# fetch messages of specific channel
	ch = 1
	channel = Channel.query.get(ch)
	mes_list = [m.message for m in Message.messages_by_channel(ch)]
	print(f'\nAll Chats for "{channel.channel}"')
	print(mes_list)



if __name__ == "__main__":
    with app.app_context():
        read()
