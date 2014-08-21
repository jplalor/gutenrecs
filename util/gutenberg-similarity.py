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
loader = scipy.io.mmread("testfile_old.mtx")
new_matrix = loader.tocsr()

print "loading books"
loader2 = numpy.loadtxt('doc_names.txt', delimiter=',', dtype="string")

print "convert to list"
doc_names_pre = loader2.tolist()

print "formatting"
doc_names = [format_name(x) for x in doc_names_pre]

count = 0
results = []
for book in doc_names:
    similarities = cosine_similarity(new_matrix[count:count+1], new_matrix)
    #20 results per book
    books = similarities.argsort()[0][-21:-1]
    for i in reversed(books):
        results.append([book, doc_names[i], similarities[0][i]])
    count +=1

numpy.savetxt("similarities.txt",doc_names,delimiter = ',', fmt="%s")