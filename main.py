from preprocess import *
from inverted_index import *

#this file will generate the preprocessed documents and Inverted index along with vector space model

def main():
    preproc = readfiles()
    file = index_create(preproc)
    
    with open("stemmed_docs.txt", "w",encoding='UTF-8') as file:
        file.write(str(preproc))
        file.write("\n")

if __name__ == '__main__' :
	main()
