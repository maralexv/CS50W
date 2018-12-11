import os

from flask import Flask, request, session, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(16)
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# Home Page
@app.route("/", methods=['POST'])
def index():

	# if user is logged in
	if 'username' in session:
        return f'Logged in as {escape(session['username'])}'

	# if user is NOT logged in
	return 'You are not logged in'

	# search a book (by ISBN, Title or Author)

	# list the books from search


    return render_template("index.html", username=session["username"], books=session["books"])


# Book Page
@app.route("/book", )
def book():

	# details abot the book

	# av.rating fro goodreads and number of ratings

	# review submission	

	return render_template("book.html")


# User Registration Page
@app.route("/register", methods=['POST'])
def registration():

	# registraton form

	# set user to logged-in

		redirect(url_for('index'))

	render_template("register.html")


# User logout
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


#Page Not Found Error
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404


#Restricted area, unauthorised access attempt
@app.errorhandler(401)
def page_not_found(error):
	return render_template("401.html"), 401



if __name__ == "__main__":
	app.run(debug=True)
