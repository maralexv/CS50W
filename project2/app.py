from flask import Flask, session, render_template, request, redirect, url_for, json, g
from appfactory import app, db
from appfactory.models import *
from flask_socketio import SocketIO, emit


socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/channels", methods=["POST"])
def channels():    

	username = request.form.get('username')
	user = User.query.filter_by(name=username).first()

	if user is None:
		User.add_user(username)
	
	user = User.query.filter_by(name=username).first()
	session['user_id'] = user.id
	g.user = user
	channels = Channel.channels_list()

	return json.jsonify({'user': True, 'username': g.user.name, 'channels': channels})


@app.route("/newtopic", methods=["POST"])
def newtopic():

	error = None
	
	newchannel = request.form.get('newchannel')
	channel = Channel.query.filter_by(channel=newchannel).first()

	if channel is None:
		Channel.add_channel(newchannel)
	else:
		error = 'This channel already exists!'

	channel = Channel.query.filter_by(channel=newchannel).first()
	g.channel = channel
	# messages = [m.message for m in Message.messages_by_channel(g.channel.id)]

	if error is None:
		return json.jsonify({'channel': g.channel.channel})
	else:
		return json.jsonify({'channel': error})


@app.route("/messages", methods=["POST"])
def messages():

	error = None
	channel = request.form.get('channel')
	channel = Channel.query.filter_by(channel=channel).first()

	if channel is None:
		error = 'Something went wrong - can not find the chat channel in db.'
	else:
		g.channel = channel
		messages = []
		for m in Message.messages_by_channel(g.channel.id):
			user = User.query.get(m.user_id).name
			timestamp = m.date_time
			text = m.message
			mes = {'user': user, 'timestamp': timestamp, 'text': text}
			messages.append(mes)

	if error is None:
		return json.jsonify({'me': g.user.name, 'channel': g.channel.channel, 'messages': messages})
	else:
		return json.jsonify({'channel': error, 'messages': 'No messages.'})

@socketio.on("send message")
def broadcast(data):

	userid = User.query.filter_by(name=data["message"]["user"]).first().id
	channelid = Channel.query.filter_by(channel=data["message"]["channel"]).first().id
	text = data["message"]["text"]
	Message.add_mes(text, userid, channelid)

	number_of_messages = len(Message.query.all())
	first = Message.query.all()[0]
	if number_of_messages > 100:
		db.session.delete(first)
		db.session.commit()

	last = Message.query.all()[-1]
	user = User.query.get(last.user_id).name
	timestamp = last.date_time.strftime("%a, %d %b %Y %H:%M:%S")
	text = last.message
	emit('broadcast message', {'user': user, 'timestamp': timestamp, 'text': text}, broadcast=True)


# Make sure g.user is loaded before every request
@app.before_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = User.query.get(user_id)


if __name__ == '__main__':
    socketio.run(app)
