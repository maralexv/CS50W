import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database engine object from SQLAlchemy that manages connections to the database
# DATABASE_URL is an environment variable that indicates where the database lives
engine = create_engine(os.getenv("DATABASE_URL")) 	
                                      
# Create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))    	
                                               		
# initiate variable f that will be storring the books.csv file data for import
f = open("static/books.csv")
reader = csv.reader(f)
count = 0
# Add data from .csv file to SQL Database (db)
# for loop gives each column a name
for isbn, title, author, year in reader: 
	# values are assigned placeholders and then values are added (incerted) into table 
	db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
              {"isbn": isbn, "title": title, "author": author, "year": year})
	count = count + 1

# transactions are assumed, close the transaction 
db.commit() 

print(f"Added {count} rows to the books table.")

