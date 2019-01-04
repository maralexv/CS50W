# Project 1

This is a small Flask App developed as an exercise for project1 at SC50W course. 

The web app is a book review website, where users can register and revoew books from predefined library of 5000 items. Any registered user can search the library by book title, author or ISBN. Once a book is selected, user can rate it (1-5) and leave a review for the book (only one review per book per user is possible).

Users can login and logout, view their profile, where their data and all their reviews are displayed. There, user can delete his/her profiel together with all his/her book reviews.

Finally, Goodreads API is used to fetch Goodreds rating for books basd on ISBN (if available). The 'api' for this app is created as view. Anyone, folowing the link/api/<isbn> would get the json file with book title, author, publishing year, ISBN, average score and times the book was rated on this website.

All db handling and views are in one app.py (no blueprints used for this app). 
    
Here is the app structure:

```bash
├── README.md
├── app.py
├── requirements.txt
├── static
│   ├── books.png
│   ├── source_files
│   │   ├── apitest.py
│   │   ├── books.csv
│   │   ├── data_import.py
│   │   ├── db.txt
│   │   └── goodreads_api_key.txt
│   └── style.css
└── templates
    ├── 401.html
    ├── 404.html
    ├── base.html
    ├── book.html
    ├── index.html
    ├── login.html
    ├── register.html
    └── userprofile.html
```
