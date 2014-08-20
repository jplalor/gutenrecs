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
app.debug = True


def format_name(filename):
    if (filename.find('-') > -1):
        booknum = filename[:filename.index('-')]
    else:
        booknum = filename[:filename.index('.')]
    return str(booknum)


@app.route('/')
def index():	
    return render_template('index.html')


@app.route('/searchbook/', methods=['GET', 'POST'])
def searchbook():
	
    #indexfile = "C:\\Users\\Kaitlin\\Documents\\depaul\\gutenberg\\"
    loader = scipy.io.mmread("testfile.mtx")

    book_name = request.args.get('search','')

    num_results = int(request.args.get('numhits',''))

    loader2 = numpy.loadtxt('doc_names.txt', delimiter=',', dtype="string")
    
    doc_names_pre = loader2.tolist()

    doc_names = [format_name(x) for x in doc_names_pre]

    choice = doc_names.index(book_name)

    new_matrix = loader.tocsr()
    # will need to load the book titles somehow
    
    similarities = cosine_similarity(new_matrix[choice:choice+1], new_matrix)
    print(similarities)
    books = similarities.argsort()[0][-(num_results+1):-1]

    results = []

    for i in reversed(books):
        results.append([doc_names[i], similarities[0][i]])
    
    return render_template('searchbook.html', similarities=results)


if __name__ == '__main__':
    app.run(debug=True)

