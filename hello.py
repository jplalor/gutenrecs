#websiteeeeeeeeeeeeeee
import os
import io
import scipy
import scipy.io
import numpy
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from flask import Flask, render_template, request
app = Flask(__name__)
#app.debug = True



@app.route('/')
def index():	
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)

