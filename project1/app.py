import os

from flask import Flask, request, session, render_template, redirect, url_for, flash, g
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


#############    VIEWS   #################


# Home Page
@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        query = request.form.get('query')

        error = None
        quantity = None

        books = db.execute('SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author',
            {'isbn': '%'+query+'%', 'title': '%'+query+'%', 'author': '%'+query+'%'}
            ).fetchall()

        if books == []:
            error = 'Sorry, there are no such books in my Library. Please try anothere search.'
        
        if error is None:
            session['books'] = books
            g.books = books
            quantity = len(books)

            return render_template("index.html", books=session['books'], quantity=quantity)

        flash(error)

    return render_template("index.html")


# Book Page
@app.route("/book/<int:id>/")
def book(id):

    # error = None

    # # fetch the book from db
    # book = db.execute('SELECT * FROM books WHERE id = :id', {'id': book_id}).fetchone()
    # session['book'] = book
    # g.book = book

	# av.rating from this website users and number of ratings

	# av.rating from goodreads and number of ratings

	# for for user to provide reating and review	
    
    return render_template("book.html", id=id)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        userpassword = request.form.get('userpassword')

        error = None
        user = db.execute('SELECT * FROM users WHERE username = :username', {'username': username}
            ).fetchone()

        if user is None:
            error = 'Account does not exist or incorrect Username.'
        elif user['userpassword'] != userpassword:
            error = 'Incorrect Password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            g.user = user

            return redirect(url_for('home'))

            '''
            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # Now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('home')

            return redirect(next, user=session['user'])
            '''

        flash(error)

    return render_template("login.html")


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute('SELECT * FROM users WHERE id = :id', {'id': user_id}).fetchone()


# User Registration Page
@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = " ".join([x.capitalize() for x in request.form.get("name").split()])
        username = request.form.get("username")
        useremail = request.form.get("useremail")
        userpassword = request.form.get("userpassword")

        error = None

        if not username:
            error = 'Username is required.'
        elif not useremail:
        	error = 'Email is required.'
        elif not userpassword:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = :username', {'username': username}
            ).fetchone() is not None:
            error = f'User "{username}" is already registered.'
        elif db.execute(
            'SELECT id FROM users WHERE useremail = :useremail', {'useremail': useremail}
            ).fetchone() is not None:
            error = f'User with email {useremail} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO users (name, username, useremail, userpassword) VALUES (:name, :username, :useremail, :userpassword)',
                {'name': name, 'username': username, 'useremail': useremail, 'userpassword': userpassword}
                )
            db.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template("register.html")


# User profile
@app.route('/userprofile')
def userprofile():

    render_template('userprofile.html')


# User logout
@app.route('/logout')
def logout():
    # remove user from the session if it's there
    session.pop('user_id', None)
    session.pop('books', None)
    session.pop('book', None)
    # flush g variable
    g.user = None
    g.books = None
    g.book = None
    return redirect(url_for('home'))


# Page Not Found error
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404


# Unauthorised access attempt error
@app.errorhandler(401)
def unauthorised(error):
	return render_template("401.html"), 401


# Run the App
if __name__ == "__main__":
	app.run(debug=True)
