
#Aggregate the meta-data for each book.
import csv
import os
import pprint
from rdflib import Graph, URIRef


#need to strip filename for ID
#figure out the correct author agent (look at an old one)

output = open('metadata.csv', 'wb')
writer = csv.writer(output)

writer.writerow(['BookID', 'Title', 'Author', 'Downloads'])
outputdir = 'C:\\Users\\John Lalor\\Documents\\DePaul\\ECT584\\gutenberg\\rdf-files.tar\\cache\\epub'

for dirname, dirnames, filenames in os.walk('C:\\Users\\John Lalor\\Documents\\DePaul\\ECT584\\gutenberg\\rdf-files.tar\\cache\\epub'):
    for fname in filenames:
    	print "working on " + fname
    	fpath = os.path.join(outputdir,dirname, fname)
        g = Graph()
        g.parse(fpath)
        title = 'None'
        author = 'None'
        downloads = '0'
        #title1 = URIRef('http://www.gutenberg.org/ebooks/1018')
        title2 = URIRef('http://purl.org/dc/terms/title')
        #author1 = URIRef('http://www.gutenberg.org/2009/agents/344')
        author2 = URIRef('http://www.gutenberg.org/2009/pgterms/name')
        #downloads1 = URIRef('http://www.gutenberg.org/ebooks/1018')
        downloads2 = URIRef('http://www.gutenberg.org/2009/pgterms/downloads')
        for s,p,o in g.triples((None, title2, None)):
            title = o.encode('utf8', 'ignore')
        for s,p,o in g.triples((None, author2, None)):
            author = o.encode('utf8', 'ignore')
        for s,p,o in g.triples((None, downloads2, None)):
            downloads = o.encode('utf8', 'ignore')

        book = fname[2:-4]
        #title = g.value(subject=title1, predicate=title2)
        #author = g.value(subject=author1, predicate=author2)
        #downloads = g.value(subject=downloads1, predicate=downloads2)
        print "writing " + book + "," + title + "," + author + "," + downloads
        writer.writerow([book,title,author,downloads])

output.close()
