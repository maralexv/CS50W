from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from appfactory import app, db
from appfactory.models import *

db.init_app(app)

def read():
	''' read and report back from db tables '''

	# fetch all the users
	users = User.users_list() 
	print('\nAll Users:')
	print(users)


	# fetch the chat channels
	channels = Channel.channels_list()
	print('\nAll Chat Channels:')
	print(channels)

	# fetch messages of specific user
	u = 3
	channels_list = Message.channels_by_user(u)
	print(f'\nAll Chat Channels for User {u}')
	print(channels_list)

	# fetch messages of specific channel
	ch = 1
	channel = Channel.query.get(ch)
	mes_list = [m.message for m in Message.messages_by_channel(ch)]
	print(f'\nAll Chats for "{channel.channel}"')
	print(mes_list)



if __name__ == "__main__":
    with app.app_context():
        read()

