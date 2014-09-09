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
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy, desc

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
        return '<Book %r>' % self.title

@app.route('/')
def index():	
    style = url_for('static', filename='site.css')
    controller = url_for('static', filename='controller.js')
    bootstrap = url_for('static', filename='ui-bootstrap-0.9.0.min.js')
    bootstraptpls = url_for('static', filename='ui-bootstrap-tpls-0.9.0.min.js')
    
    return render_template('index.html',
        controller=controller,
        style=style,
        bootstrap=bootstrap,
        bootstraptpls=bootstraptpls
        )


@app.route('/searchbook/', methods=['GET', 'POST'])
def searchbook():
	
    #load in the searched book id
    book_name = request.args.get('search','')
    results = []

    #load the similarities flat file
    similarities = numpy.loadtxt('similarities.txt', delimiter=',', dtype="string")

    #find all similarities for the given book (20 per book)
    for a in similarities:
        if(a[0] == book_name):
            results.append(a)

    #return the results to the page (to be rendered by the template engine)
    return render_template('searchbook.html', similarities=results, selection = book_name)

@app.route('/getbooks/', methods=['GET','POST'])
def getbooks(text):
    results = []
    books = Book.filter((Book.title.beginswith(text))|(Book.author.beginswith(text))).order_by(desc(User.downloads).limit(20).all()
    for book in books:
        results.add(book.id, book.title, book.author)
    return results

if __name__ == '__main__':
    app.run(debug=True)

