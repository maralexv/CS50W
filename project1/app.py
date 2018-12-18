import os

from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Initialise the App
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


##########################################
#############    VIEWS   #################
##########################################

# Home Page
@app.route("/")
def home():
	
	# form to search a book (by ISBN, Title or Author)

	# list the most popular books from Goodreads

    return render_template("index.html")


# Book Page
@app.route("/book")
def book():
	error = None
	# check if user is logged-in
	if 'username' in session:
        user = session['username']
    else:
    	error = 'You are not logged-in.'


	# provide details about the book

	# av.rating from this website users and number of ratings

	# av.rating from goodreads and number of ratings

	# review submission	

	return render_template("book.html")


# User login
@app.route('/login')
def login():
	
	if request.method == 'POST':
        username = request.form['username']
        userpassword = request.form['userpassword']
        # db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?, userpassword = ?', 
            (username, userpassword)).fetchone()

        if user is None:
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return redirect(url_for('index'))


# User Registration Page
@app.route("/register", methods=['GET', 'POST'])
def register():

	if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']
        # db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not useremail:
        	error = 'Email is required.'
        elif not userpassword:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'
        elif db.execute(
            'SELECT id FROM users WHERE useremail = ?', (useremail,)
        ).fetchone() is not None:
            error = f'User with email {useremail} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO users (username, useremail, userpassword) VALUES (?, ?, ?)',
                (username, useremail, userpassword)
            )
            db.commit()
            return redirect(url_for('login'))

        flash(error)

	render_template("register.html")


# User logout
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# Page Not Found error
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404


# Restricted area, unauthorised access attempt
@app.errorhandler(401)
def unauthorised(error):
	return render_template("401.html"), 401


# Run the App
if __name__ == "__main__":
	app.run(debug=True)
