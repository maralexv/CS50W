# import requsts
from flask import Flask, render_template, request, url_for, g, flash, session, redirect, json
from appfactory import app, login_manager
from appfactory.models import *
from flask_socketio import SocketIO, emit


socketio = SocketIO(app)


@app.route("/")
def index():



    return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=True)
