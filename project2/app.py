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
	channels = Message.channels_by_user(session['user_id'])

	return json.jsonify({'user': True, 'username': user.name, 'channels': channels})


@app.route("/messages", methods=["POST"])
def messages():
	
	pass


# Make sure g.user is loaded before every request
@app.before_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = User.query.get(user_id)


if __name__ == '__main__':
	app.run(debug=True)
