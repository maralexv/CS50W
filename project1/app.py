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


######################    VIEWS   ######################

# Home Page
@app.route("/", methods=['GET', 'POST'])
def home():
    '''
    Home page with form to search the book library
    '''
    # Simple form that accepts one query for all argumants
    if request.method == 'POST':
        query = request.form.get('query')

        error = None
        quantity = None

        # Fetch all the books, satisfying to search 
        books = db.execute('SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author ORDER BY author',
            {'isbn': '%'+query+'%', 'title': '%'+query+'%', 'author': '%'+query+'%'}
            ).fetchall()

        if books == []:
            error = 'Sorry, there are no such books in my Library. Please try anothere search.'
        
        # Load the books into session
        if error is None:
            session['books'] = books
            g.books = books
            quantity = len(books)

            return render_template("index.html", books=session['books'], quantity=quantity)

        flash(error)

    return render_template("index.html")


# Book Page
@app.route("/book/<int:bookid>/", methods=['GET', 'POST'])
def book(bookid):
    '''
    Dual purpose view: displays book informaiton, 
    and provides possibilty for user to review the book 
    '''

    # Form for book review, will be displaied if user's review for this book doesn't exist
    if request.method == 'POST':
        rtg = request.form.get('rating')
        rvw = request.form.get('review')

        if not rtg:
            flash('Please rate the book. Rating is required.')
        else:
            db.execute('INSERT INTO ratings (rating, book_id, user_id, review) VALUES (:rating, :book_id, :user_id, :review)',
                {'rating': rtg, 'book_id': bookid, 'user_id': int(session['user_id']), 'review': rvw}
                )
            db.commit()
            return redirect(url_for('book', bookid=bookid))

    # Fetch the book from db to be passed to the html for display on the page
    book = db.execute('SELECT * FROM books WHERE id = :id', {'id': bookid}).fetchone()
    g.book = book

    # User rating and review for this book, will be displaied if exists
    usereval = db.execute('SELECT * FROM ratings WHERE user_id = :user_id AND book_id = :book_id', 
        {'user_id': g.user.id, 'book_id': bookid}
        ).fetchone()

	# Book's av.rating from this website users, number of ratings, all reviews
    avrating = db.execute('SELECT AVG(rating) FROM ratings WHERE book_id = :book_id',
        {'book_id': bookid}
        )
    numrating = db.execute('SELECT COUNT(*) FROM ratings WHERE book_id = :book_id',
        {'book_id': bookid}
        )

    if avrating == [] or numrating == []:
        avrating = 'This book has not been rated yet.'
        numrating = 0

    # Fetch all the reviews for tghe book with users
    reviews = db.execute('SELECT review FROM ratings WHERE book_id = :book_id',
        {'book_id': bookid}
        )

    # av.rating from goodreads and number of ratings

    # form for user to provide reating and review
    
    return render_template("book.html", bookid=bookid, book=book, usereval=usereval, reviews=reviews)


# User Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Login form - get the form data
    if request.method == 'POST':
        username = request.form.get('username')
        userpassword = request.form.get('userpassword')

        error = None

        # Fetch the user data form db
        user = db.execute('SELECT * FROM users WHERE username = :username', {'username': username}
            ).fetchone()

        # Manage error messages
        if user is None:
            error = 'Account does not exist or incorrect Username.'
        elif user['userpassword'] != userpassword:
            error = 'Incorrect Password.'

        # Login user = get the user into session
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


# Make sure g.user is loaded before every request
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
    '''
    Regiser User and redirect to Login page
    '''

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


# User Profile
@app.route('/userprofile')
def userprofile():
    '''
    Display user account/profile and give option to update or delete it
    '''

    render_template('userprofile.html')


# User Logout
@app.route('/logout')
def logout():
    # remove user, books from the session if it's there
    session.pop('user_id', None)
    session.pop('books', None)
    # flush g variables
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
