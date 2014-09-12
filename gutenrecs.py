#websiteeeeeeeeeeeeeee
import os
import io
import scipy
import scipy.io
import numpy
import csv
import json
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from flask import Flask, render_template, request, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy #, desc
from sqlalchemy import desc

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)

#app.debug = True

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False)
    author = db.Column(db.String(200), unique=False)
    downloads = db.Column(db.Integer, unique=False)

    def __init__(self, id, title, author, downloads):
        self.id = id
        self.title = title
        self.author = author
        self.downloads = downloads

    def __repr__(self):
        return '<%r by %r>' % (self.title,  self.author)

    def to_json(self):
        return dict(id=self.id,
                    title=self.title,
                    author=self.author,
                    downloads=self.downloads)

@app.route('/')
def index():	
    style = url_for('static', filename='site.css')
    controller = url_for('static', filename='controller.js')
    bootstrap = url_for('static', filename='ui-bootstrap-0.10.0.js')
    bootstraptpls = url_for('static', filename='ui-bootstrap-tpls-0.9.0.min.js')
    
    return render_template('index.html',
        controller=controller,
        style=style,
        bootstraptpls=bootstraptpls
    )

@app.route('/gutenrecs')
def gutenrecs():	 
    style = url_for('static', filename='site.css')
    controller = url_for('static', filename='controller.js')
    bootstrap = url_for('static', filename='ui-bootstrap-0.10.0.js')
    bootstraptpls = url_for('static', filename='ui-bootstrap-tpls-0.9.0.min.js')
    
    return render_template('gutenrecs.html',
        controller=controller,
        style=style,
        bootstraptpls=bootstraptpls
    )

@app.route('/searchbook/<bookid>', methods=['GET', 'POST'])
def searchbook(bookid):
    style = url_for('static', filename='site.css')
    controller = url_for('static', filename='controller.js')
    bootstrap = url_for('static', filename='ui-bootstrap-0.10.0.js')
    bootstraptpls = url_for('static', filename='ui-bootstrap-tpls-0.9.0.min.js')
	
    #load in the searched book id
    #book_name = request.args.get('search','')
    book_name = bookid
    results = []
    searched_book = Book.query.filter_by(id=bookid).first().title

    #load the similarities flat file
    similarities = numpy.loadtxt('similarities.txt', delimiter=',', dtype="string")

    #find all similarities for the given book (20 per book)
    for a in similarities:
        if(a[0] == book_name):
            book_result = Book.query.filter_by(id=a[1]).first()
            results.append(book_result.to_json())

    #return the results to the page (to be rendered by the template engine)
    return render_template('searchbook.html', similarities=results, selection = searched_book,
	controller=controller,
    style=style,
    bootstraptpls=bootstraptpls
	)

@app.route('/getbooks/<text>', methods=['GET','POST'])
def getbooks(text):
    results = []
    books = Book.query.filter((Book.title.startswith(text))|(Book.author.startswith(text))).order_by(desc(Book.downloads)).limit(20).all()
    #print books.to_json()
    for book in books:
        #print book.to_json()
        results.append(book.to_json())
    #result = [b.__dict__ for b in books]
    #return jsonify(result=result)
    return jsonify(data=results)

if __name__ == '__main__':
    app.run(debug=True)

