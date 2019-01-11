# import requsts
from flask import Flask, session, render_template, request, redirect, url_for, json
from appfactory import app, db
from appfactory.models import *
from flask_socketio import SocketIO, emit


socketio = SocketIO(app)


@app.route("/")
def index():



    return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=True)
