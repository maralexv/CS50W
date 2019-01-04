import os
import requests
import json
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


###########################  APIs  #################################


print('\n--------------------------------------\n')
print('my API:')
error = None
isbn = '0316780375'
# isbn = '1423102266'

jbook = db.execute('SELECT id, title, author, year, isbn FROM books WHERE isbn = :isbn', 
        {'isbn': isbn}
        ).fetchone()

if jbook is None:
	error = 404
else:
	jbookid = jbook[0]
	javr = db.execute('SELECT AVG(rating) FROM ratings WHERE book_id = :book_id',
	        {'book_id': jbookid}
	        ).fetchone()
	jnumr = db.execute('SELECT COUNT(*) FROM ratings WHERE book_id = :book_id',
	        {'book_id': jbookid}
	        ).fetchone()

if error == None:
	jbookdict = {'title': jbook.title, 'author': jbook.author, 'year': jbook.year,  'isbn': isbn, 'review_count': jnumr.count, 'average_score': str(javr.avg)}
	print(json.dumps(jbookdict, indent=4))
else:
	print("Error ", error)


print('\n--------------------------------------\n')
print('Goodreads API:')

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qXpPQv2DwijzCIgVO2BQ", "isbns": "1423102266"}).json()
grrating=res['books'][0]['average_rating']
grcount=res['books'][0]['work_ratings_count']
print(grrating)
print(grcount)
