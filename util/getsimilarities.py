from bs4 import BeautifulSoup
import requests

print 'script to pull current Project Gutenberg rec''s and store them in a file'

root_url = 'http://www.gutenberg.org/ebooks/'
page_attr = 'li.booklink a[href]'
doc = open('webSim.txt', 'w')

def getSimilarBooks(bookNum):
    pageURL = root_url + bookNum + '/also/'
    response = requests.get(pageURL)
    soup = BeautifulSoup(response.text)
    bookSim = [a.attrs.get('href')[8:] for a in soup.select(page_attr)]
    write_line = bookNum+','
    for b in bookSim:
        write_line += b+','
    doc.write(write_line+'\n')



