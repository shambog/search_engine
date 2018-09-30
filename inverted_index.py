from preprocessbk import *
import math

#creating inverted and vector space model
def index_create(text):
    #filtering distinc terms from all the documents
    distinct_words = list({terms for docs in text for terms in docs})
    distinct_words.sort()

    #saving it in a text file to facilitate query processing
    with open("distinct_words.txt", "w",encoding='UTF-8') as file:
        file.write(str(distinct_words))
        file.write("\n")

    #creating inverted index    
    inverted_index = {terms: [docs.count(terms) for docs in text] for terms in distinct_words}

    #saving it in a text file to facilitate query processing
    with open("inverted_index.txt", "w",encoding='UTF-8') as file:
        file.write(str(inverted_index))
        file.write("\n")

    #creating idf for each term    
    idf = {terms:round(math.log10(float(len(text))/float(len([df for df in list_process if df > 0]))),3) for terms,list_process in inverted_index.items()}

    #saving it in a text file to facilitate query processing
    with open("idf.txt", "w",encoding='UTF-8') as file:
            file.write(str(idf))
            file.write("\n")

    #creating vector space of each document        
    vector_space, temp = [], []
    for docs in text:
        for terms in distinct_words:
            temp.append(idf[terms]*(docs.count(terms)))
        vector_space.append(temp)
        temp = []

    #normalizing the document vector    
    docs_temp, normalized_vector_space = [], []
    for docs in vector_space:
        temp = 0
        for val in docs:
            temp += (val**2)
        temp = (temp**0.5)
        for val in docs:
            docs_temp.append(round(val/temp,3))
        normalized_vector_space.append(docs_temp)
        docs_temp = []

    #saving it in a text file to facilitate query processing    
    with open("vector_space.txt", "w",encoding='UTF-8') as file:
            file.write(str(normalized_vector_space))