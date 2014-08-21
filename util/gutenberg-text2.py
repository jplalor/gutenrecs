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


# need to loop through the files and create a list of content
corpus = []
doc_names = []
book_names = []

vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 18, 
                                non_negative=True, stop_words='english', norm=None)

transformer = TfidfTransformer()

#then do the hard work


outputdir = "C:\\Users\\John Lalor\\Documents\\DePaul\\ECT584\\gutenberg\\working\\"

#outputdir = "C:\\Users\\Kaitlin\\Documents\\depaul\\gutenberg\\reprojectsteps\\"

count = 0
total = 0
run = 1
first_run = True
print "Begin file loads"

for f in os.listdir(outputdir):
    total += 1
    fpath = os.path.join(outputdir, f)
    if(total == 5001):
        print "exiting loop"
        break;
    try:
        if (os.path.isfile(fpath)):
            with open(fpath) as f2:
                content = f2.readlines()
                content = ', '.join(content)
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
                    z = vectorizer.transform(corpus)
                    if(first_run):
                        working_matrix = z
                        #scipy.io.mmwrite("testfile",working_matrix)
                        first_run = False
                        #print (working_matrix)
                    else:
                        print "stacking..."
                        working_matrix = vstack([working_matrix,z])
                        #scipy.io.mmwrite("testfile",working_matrix)
                    corpus = []
    except Exception, e:
        print e
#need to catch the last few files
z = vectorizer.transform(corpus)
working_matrix = vstack([working_matrix,z])
#scipy.io.mmwrite("testfile",working_matrix)
tfidf_model = transformer.fit_transform(working_matrix)
                    #if(first_run):
 
                    #else:
                        #working_matrix = vstack([working_matrix,z])


#scipy.io.mmwrite("testfile",working_matrix)
scipy.io.mmwrite("tfidf_file",tfidf_model)
numpy.savetxt("book_names.txt",book_names,delimiter = ',', fmt="%s")
numpy.savetxt("doc_names.txt",doc_names,delimiter = ',', fmt="%s")


def format_name(filename):
    if (filename.find('-') > -1):
        booknum = filename[:filename.index('-')]
    else:
        booknum = filename[:filename.index('.')]
    return str(booknum)
print "loading matrix"
#loader = scipy.io.mmread("testfile_old.mtx")
new_matrix = tfidf_model.tocsr()

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

numpy.savetxt("similarities.txt",results,delimiter = ',', fmt="%s")



