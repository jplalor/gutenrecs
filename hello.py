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

app = Flask(__name__)
#app.debug = True



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
    csvfile =  open('metadata.csv', 'rb') 
    count = 0
    
    fieldnames = ('BookID','Title','Author','Downloads')
    reader = csv.DictReader(csvfile, fieldnames)
    out = json.dumps([row for row in reader ])
    #return jsonify(**reader)
    return out
    #    return flask.jsonify(reader)
    #    summary = do_summary_on_file(csv)
        #return reader
        #return jsonify(csv_name=csvfile)

if __name__ == '__main__':
    app.run(debug=True)

