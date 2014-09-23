# Import the necessary libraries
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
from scipy import io

#This function standardizes the book ids based on the filename.
#some files include a -8 or -old based on their version, and they need to be removed
#also need to remove the '.txt'
def format_name(filename):
    if (filename.find('-') > -1):
        booknum = filename[2:filename.index('-')]
    else:
        booknum = filename[2:filename.index('.')]
    return str(booknum)

#The rest of this script imports the TF-IDF matrix and calculates the recommendations
print "loading matrix"
#loader = scipy.io.mmread("/home/ubuntu/gutenrecs/util/testfile_old.mtx")
loader = scipy.io.mmread("C:\\Users\\jlalor\\Documents\\gutenrecs\\util\\lda_file.mtx")


#convert the matrix to a sparse matrix using scipy
print "converting matrix"
new_matrix = loader.tocsr()
#new_matrix = loader
#load the book names so that we can match rows in the matrix with the book id
print "loading books"
loader2 = numpy.loadtxt('book_names.txt', delimiter=',', dtype="string")

#print "convert to list"
doc_names_pre = loader2.tolist()

#print "formatting"
#doc_names = [format_name(x) for x in doc_names_pre]
doc_names = doc_names_pre

#calculate the cosine similarities and find the 20 highest recommendations
print "start the similarity calculations"
count = 0
results = []
#for book in doc_names:
while count < 4:
    print "current count: " + str(count)
    similarities = cosine_similarity(new_matrix[count:count+1], new_matrix)
    #10 results per book
    #ignore the first result, which is the book itself (similarity of 1)
    books = similarities.argsort()[0][-11:-1]
    for i in reversed(books):
        results.append([doc_names[count],doc_names[i], similarities[0][i]])
        #results.append([book, doc_names[i], similarities[0][i]])
    count +=1

#save the output file.
numpy.savetxt("similarities.txt",results,delimiter = ',', fmt="%s")
