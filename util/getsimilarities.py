from bs4 import BeautifulSoup
import requests

print 'script to pull current Project Gutenberg rec''s and store them in a file'

def format_name(filename):
    if (filename.find('-') > -1):
        booknum = filename[0:filename.index('-')]
    else:
        booknum = filename[0:filename.index('.')]
    return str(booknum)

def getSimilarBooks(bookNum):
    pageURL = root_url + bookNum + '/also/'
    response = requests.get(pageURL)
    soup = BeautifulSoup(response.text)
    bookSim = [a.attrs.get('href')[8:] for a in soup.select(page_attr)]
    write_line = bookNum+','
    for b in bookSim:
        write_line += b+','
    doc.write(write_line+'\n')

root_url = 'http://www.gutenberg.org/ebooks/'
page_attr = 'li.booklink a[href]'
doc = open('webSim.txt', 'w')

book_file = open('doc_names_09252014.txt')
book_names = book_file.readlines()

for a in book_names:
    formatted_name = format_name(a)
    print 'getting results for ' + formatted_name
    getSimilarBooks(formatted_name)
