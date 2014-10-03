# code for doing necessary scikit-learn fun stuff
import os
import csv
import numpy
import scipy
import gc
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack, csr_matrix


def format_name(filename):
    if (filename.find('-') > -1):
        booknum = filename[:filename.index('-')]
    else:
        booknum = filename[:filename.index('.')]
    return str(booknum)
print "loading matrix"

#one of the following: normalizedLDA_092014.mtx, pca_file.mtx, pca_lsa_file.mtx
def calcSim(filename):

    loader = scipy.io.mmread("normalizedLDA_092014.mtx")
    new_matrix = loader

    print "loading books"
    loader2 = numpy.loadtxt('doc_names_09252014.txt', delimiter=',', dtype="string")

    print "convert to list"
    doc_names_pre = loader2.tolist()

    print "formatting"
    doc_names = [format_name(x) for x in doc_names_pre]

    count = 0
    results = []
    print "beginning similarity calculations"

    for book in doc_names:
        similarities = cosine_similarity(new_matrix[count:count+1], new_matrix)
        #20 results per book
        books = similarities.argsort()[0][-21:-1]
        for i in reversed(books):
            results.append([book, doc_names[i], similarities[0][i]])
        count +=1

    print "saving similarity file"
    numpy.savetxt("sim_"+filename+".txt",results,delimiter = ',', fmt="%s")