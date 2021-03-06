import os
import requests
from flask import Flask, request, session, render_template, redirect, url_for, flash, g, json
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
        ).fetchone()
    numrating = db.execute('SELECT COUNT(*) FROM ratings WHERE book_id = :book_id',
        {'book_id': bookid}
        ).fetchone()

    # Fetch all the reviews for tghe book with users
    reviews = db.execute('SELECT book_id, rating, review, timst, name FROM ratings JOIN users ON ratings.user_id=users.id WHERE book_id = :book_id ORDER BY timst DESC',
        {'book_id': bookid}
        )

    # av.rating and number of ratings from Goodreads
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qXpPQv2DwijzCIgVO2BQ", "isbns": book.isbn}).json()
    grrating = goodreads['books'][0]['average_rating']
    grcount = goodreads['books'][0]['work_ratings_count']


    return render_template("book.html", bookid=bookid, book=book, usereval=usereval, reviews=reviews, avrating=avrating, numrating=numrating, grrating=grrating, grcount=grcount)


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
            session['user'] = user
            g.user = user

            return redirect(url_for('home'))

        flash(error)

    return render_template("login.html")


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
@app.route('/userprofile', methods=['GET', 'POST'])
def userprofile():
    '''
    Display user account/profile and give option to delete it
    '''
    if request.method == 'POST':
        db.execute(
            'DELETE FROM ratings WHERE user_id = :user_id',
            {'user_id': g.user.id}
            )
        db.commit()
        db.execute(
            'DELETE FROM users WHERE id = :id',
            {'id': g.user.id}
            )
        db.commit()
        
        return redirect(url_for('home'))

    # All user reviews, will be displaied if exists
    userreviews = db.execute('SELECT * FROM ratings JOIN books ON books.id=ratings.book_id WHERE user_id = :user_id', 
        {'user_id': g.user.id}
        ).fetchall()

    return render_template('userprofile.html', userreviews=userreviews)


# User Logout
@app.route('/logout')
def logout():
    # remove user, books from the session if it's there
    session.pop('user_id', None)
    session.pop('user', None)
    session.pop('books', None)
    # flush g variables
    g.user = None
    g.books = None
    g.book = None
    return redirect(url_for('home'))


@app.route("/api/<isbn>")
def api(isbn):
    '''
    returns a json dictionary with data for book with given ISBN
    '''
    error = None
    jbook = db.execute('SELECT id, title, author, year, isbn FROM books WHERE isbn = :isbn', 
            {'isbn': isbn}
            ).fetchone()

    if jbook is None:
        error = "Invalid ISBN. No such book in my library."
        return json.jsonify({"error": error}), 404
    else:
        jbookid = jbook[0]
        javr = db.execute('SELECT AVG(rating) FROM ratings WHERE book_id = :book_id',
                {'book_id': jbookid}
                ).fetchone()
        jnumr = db.execute('SELECT COUNT(*) FROM ratings WHERE book_id = :book_id',
                {'book_id': jbookid}
                ).fetchone()

    if error == None:
        return json.jsonify({'title': jbook.title, 'author': jbook.author, 'year': jbook.year,  'isbn': jbook.isbn, 'review_count': jnumr.count, 'average_score': str(javr.avg)})
    else:
        return render_template("404.html"), 404


# Make sure g.user is loaded before every request
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute('SELECT * FROM users WHERE id = :id', {'id': user_id}).fetchone()


# Page Not Found error
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404


# Unauthorised access attempt error
@app.errorhandler(403)
def unauthorised(error):
	return render_template("401.html"), 403


# Run the App
if __name__ == "__main__":
	app.run(debug=True)
