from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import re
import os
from lxml.html.clean import clean_html, Cleaner

#read files from directory in a sorted manner
filelists = re.compile(r'(\d+)')
def sorted_files(value):
    splitval = filelists.split(value)
    splitval[1::2] = map(int, splitval[1::2])
    return splitval

#reading the files
def readfiles():
    dirpath = r'C:\Users\saika\AppData\Local\Programs\Python\Python36-32\Project-final\Crawled_Files'
    doclist=list()
    for files in sorted(os.listdir(dirpath), key=sorted_files):
        with open(files, 'r',encoding='UTF-8') as text_file:
            final_file=text_file.read() 
            doclist.append(preproc(final_file))
    return doclist

def preproc(file):
    
    #remove html css and js tags
    cleaner = Cleaner(embedded=True, meta=True, page_structure=True, links=True, style=True, scripts=True, javascript=True,
                      comments=True, forms=True,
                      remove_tags = ['a', 'li', 'td', 'span', 'font', 'div', 'http'])
    
    file = cleaner.clean_html(file)             #cleaned html, js and css elements
    punc = re.compile(r'[^a-zA-Z]')             #removed everything except character or words
    file = punc.sub(' ',file)
    file = re.sub( '\s+', ' ', file).strip()    #removed multiple spaces
    file = file.lower()
    file = re.sub(r'\b\w\b', '', file)
    
    tokens = word_tokenize(file)                #tokenized the words
    stop_list = set(stopwords.words("english")) # setting up list of stop words
    newfile = [w for w in tokens if not w in stop_list]

    stemmer = PorterStemmer()                   #used code for porter stemmer
    stemmed = []
    print('#15')
    for words in newfile:
        stemmed.append(stemmer.stem(words))
    return stemmed
