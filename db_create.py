#build out the database.

import os, csv
from flask.ext.sqlalchemy import sqlalchemy
from hello import db, Book

#conn = sqlite3.connect(db)
#c = conn.cursor()
#c.execute("DROP TABLE IF EXISTS book")
#c.execute("CREATE TABLE id INTEGER NOT NULL, title VARCHAR(200), author VARCHAR(200), \
#    downloads INTEGER, PRIMARY KEY(id)")

with open('metadata.csv', 'rb') as csvfile:
    dbreader = csv.reader(csvfile)
    for row in dbreader:
        bookid = unicode(row[0], encoding='utf-8')
        booktitle = unicode(row[1], encoding='utf-8')
        bookauthor = unicode(row[2], encoding='utf-8')
        bookdownloads = unicode(row[3], encoding='utf-8')
        print 'writing book id: ' + bookid + 'to database'

        book = Book(bookid, booktitle, bookauthor, bookdownloads)
        db.session.add(book)
    db.session.commit()

Book.query.all()
