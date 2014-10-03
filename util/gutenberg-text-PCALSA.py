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
from scipy.sparse import vstack, csr_matrix, hstack
from sklearn.decomposition import PCA, TruncatedSVD
from scipy import io


# need to loop through the files and create a list of content
corpus = []
doc_names = []
book_names = []

#initialize the hashing vectorizer with the relevant settings
#ignore decoding errors (like unknown characters)
#use the standard stop word list for english
#do not normalize the results (this will occur later)
vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 18, 
                                non_negative=True, stop_words='english', norm=None)

#initialize the TFIDF Transformer
#transformer = TfidfTransformer()

#initialize transformer
transformerPCA = PCA(n_components=50)
transformerLSA = TruncatedSVD(n_components=50)

#then do the hard work

#local directory to load books from (would need to be updated if run locally)
#outputdir = "C:\\Users\\John Lalor\\Documents\\DePaul\\ECT584\\gutenberg\\working\\"

outputdir = "C:\\Users\\jlalor\\Documents\\books\\"


#outputdir = "C:\\Users\\Kaitlin\\Documents\\depaul\\gutenberg\\reprojectsteps\\"


count = 0
total = 0
run = 1
first_run = True
print "Begin file loads"

#load in 5000 books, so that the resulting matrix can be loaded and used.
for f in os.listdir(outputdir):
    total += 1
    fpath = os.path.join(outputdir, f)
    #if(total == 5001):
    #    print "exiting loop"
    #    break;
    try:
        if (os.path.isfile(fpath)):
            with open(fpath) as f2:
                content = f2.readlines()
                #set the book content as a string
                content = ', '.join(content)
                #append the content to the working corpus
                corpus.append(content)
                doc_names.append(f)
                book_names.append(content[:50])
                if(count < 150):
                    count += 1
                    if(count == 75):
                        print "Halfway there..."
                else:
                    count = 0
                    print "Processing partial corpus for run " + str(run)
                    run += 1
                    #processCorpus(corpus, first_run)
                    print "transform"
                    #perform the hashing vectorization on the working corpus
                    z = vectorizer.transform(corpus)
                    if(first_run):
                        working_matrix = z
                        #scipy.io.mmwrite("testfile",working_matrix)
                        first_run = False
                        #print (working_matrix)
                    else:
                        #append the new matrix to the existing compilation of the matrix
                        print "stacking..."
                        working_matrix = vstack([working_matrix,z])
                        #scipy.io.mmwrite("testfile",working_matrix)
                    corpus = []
    except Exception, e:
        print e
#need to catch the last few files
z = vectorizer.transform(corpus)
working_matrix = vstack([working_matrix,z])
working_matrix = z


#this is commented out as it is a huge memory drain, and unneccessary at this point
#scipy.io.mmwrite("testfile",working_matrix)
#perform the tfidf transformation on the entire term count matrix
#tfidf_model = transformer.fit_transform(working_matrix)
pca_model = transformerPCA.fit_transform(working_matrix)      
lsa_model = transformerLSA.fit_transform(working_matrix)              


#write the results to disk to be used in gutenberg-similarity.py
pca_file_sparse = scipy.sparse.csr_matrix(pca_model)
lsa_file_sparse = scipy.sparse.csr_matrix(lsa_model)

final_matrix = hstack([pca_file_sparse, lsa_file_sparse])
scipy.io.mmwrite("pca_file",final_matrix)

#numpy.savetxt("book_names.txt",book_names,delimiter = ',', fmt="%s")
#numpy.savetxt("doc_names.txt",doc_names,delimiter = ',', fmt="%s")




