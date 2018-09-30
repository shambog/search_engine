from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import *
from nltk.stem.porter import *
import re

#preprocessing and stemming query terms
def call_func(text):
    try:
        tokens = word_tokenize(text)                            #tokenizing query terms
        stop_list = set(stopwords.words("english"))             # setting up list of stop words
        newtext = [w for w in tokens if not w in stop_list]

        stemmer = PorterStemmer()                               #stemming query terms using Porter Stemmer
        stemmed = []
        for words in newtext:
            stemmed.append(stemmer.stem(words))
        return query_create(stemmed)                            #after done call the query processing function
    except (TypeError,ValueError):
        pass

#function to process query
def query_create(query):

#reading all text files from repository        
        with open("vector_space.txt") as file:
            normalized_vector_space = eval(file.read())

        with open("idf.txt") as file:
            idf = eval(file.read())

        with open("distinct_words.txt") as file:
            distinct_words = eval(file.read())

        with open("stemmed_docs.txt") as file:
            docs_list = eval(file.read())

        with open("doc_url_details.txt") as file:
            docs_links = file.read().split()

#create a sort list of distinct query terms from the user input query        
        distinct_query_terms = list({terms for terms in query})
        distinct_query_terms.sort()

#creating query vector
        vector_space_query = []
        for terms in distinct_words:
            vector_space_query.append(idf[terms]*(distinct_query_terms.count(terms)))

#creating normalized query vector
        temp = 0
        normalized_vector_space_query = []
        for val in vector_space_query:
            temp += (val**2)

        try:
        	temp = (temp**0.5)
        	for val in vector_space_query:
                    normalized_vector_space_query.append(round(val/temp,3))
        except ZeroDivisionError:
         	final_result = []
         	final_result.append("No Result Found")
         	return final_result   	

#writing normalised query vector to text file for fast processing during relevance feedback
        with open("vector_space_query.txt", "w") as file:
            file.write(str(normalized_vector_space_query))

#computing similarity cosine
        similarity_cosine = []
        for doc in normalized_vector_space:
            counter, value = 0, 0
            while counter < len(doc):
                value += round(doc[counter]*normalized_vector_space_query[counter],3)
                counter += 1
            similarity_cosine.append(value)


        sorted_similarity_cosine = similarity_cosine.copy()
        sorted_similarity_cosine.sort(reverse = True)

#commented
#printing cosine similarity results for comparison        
'''
        print("\nThe Results are:")
        generator = (val for val in sorted_similarity_cosine if val > 0)
        for val in generator:
            print(f"Document No : {similarity_cosine.index(val) + 1}")   
'''
#commented

#computing term proximity score
        improve_result = []
        value_list = []
        generator = (val for val in sorted_similarity_cosine if val > 0)									#considering top non zero cosine similar documents
        for val in generator:
            doc_index = similarity_cosine.index(val)
            if val in value_list:																			#if similar cosine values are encountered look for next document no
                counter_index = 0
                counter_index = value_list.count(val)
                while(counter_index != 0):
                    doc_index = similarity_cosine.index(val, doc_index +1)
                    counter_index -= 1
            value_list.append(val)
                    
            count, freq, query_index = 0 ,0, 0
            while(query_index < len(query) - 1 ):															#look for pairs of query terms for the entire length of query
                term_index = -1
                try:
                    term_index = docs_list[doc_index].index(query[query_index])								#find the first occurance of the query term pair in the document
                    count = term_index + 1
                    check = 1
                    freq = 0
                    while(count < len(docs_list[doc_index])):												#search through the entire length of the documents for each pair of query terms
                        if(docs_list[doc_index][count] != query[query_index]):
                            if(docs_list[doc_index][count] == query[query_index + 1]):
                                freq += 1																	#if found increment frequency counter
                                term_index = -1
                                try:
                                    term_index = docs_list[doc_index].index(query[query_index], count + 1)
                                    count = term_index + 1
                                except ValueError:
                                    break
                            elif (check > 3):																#gap between each query term of a pair should of max 3
                                term_index = -1
                                try:
                                    term_index = docs_list[doc_index].index(query[query_index], count + 1)
                                    count = term_index + 1
                                except ValueError:
                                    break
                            else:																			#continue search till a break clause from the above is encountered
                                check += 1
                                count += 1

                        else:
                            count += 1

                except ValueError:
                    query_index += 1

                query_index += 1

                
            #create a list with the document no and the freq of the pair of query terms in that document    
            improve_result.append([doc_index, freq])
            freq = 0
            
        #sort the list with non increasing freq    
        improve_result = {val[0]:val[1] for val in improve_result}
        improve_result = sorted(improve_result, key=improve_result.get, reverse = True)

        #return the final list reading the link and document name according to the above rank
        final_result = []
        count = 0
        for val in improve_result:
            if(count > 10):
                break
            else:   
                final_result.append(docs_links[2*val])
                final_result.append(docs_links[(2*val) + 1])
                count +=1
                
        return final_result


#relevance feedback taking user input of the document name
def relevance_feedback(doc_name):

        #reading vector space and query vector files
        with open("vector_space.txt") as file:
            normalized_vector_space = eval(file.read())

        with open("vector_space_query.txt") as file:
            normalized_vector_space_query = eval(file.read())

        #reading document and URL name file    
        with open("doc_url_details.txt") as file:
                docs_links = file.read().split()    

        doc_no = int(docs_links.index(doc_name) / 2) + 1
        
        #computing new query vector
        new_query = []
        counter = 0
        for val in normalized_vector_space[doc_no - 1]:
            new_query.append(normalized_vector_space_query[counter] + 0.5*val)
            counter += 1

        #computing its normalised vector    
        temp = 0
        normalized_new_query = []
        for val in new_query:
            temp += (val**2)

        temp = (temp**0.5)
        for val in new_query:
            normalized_new_query.append(round(val/temp,3))

        #calculating new sorted similarity cosine using Rochio's Algorithm    
        new_similarity_cosine = []
        for doc in normalized_vector_space:
            counter, value = 0, 0
            while counter < len(doc):
                value += round(doc[counter]*normalized_new_query[counter],3)
                counter += 1
            new_similarity_cosine.append(value)


        sorted_new_similarity_cosine = new_similarity_cosine.copy()
        sorted_new_similarity_cosine.sort(reverse = True)

        #two documents with similar cosine values should be ordered accordingly
        final_result = []
        count = 1
        value_list = []
        flag = False
        generator = (val for val in sorted_new_similarity_cosine if val > 0)
        for val in generator:
            if count > 10:
                break
            else:
                doc_index = new_similarity_cosine.index(val)
                if val in value_list:
                    counter_index = 0
                    counter_index = value_list.count(val)
                    while (counter_index != 0):
                        try:
                            doc_index = new_similarity_cosine.index(val, doc_index + 1)
                            counter_index -= 1
                        except ValueError:
                            flag = True
                            break
                value_list.append(val)

                #return the final list reading the link and document name according to the above rank
                if(flag == False):               
                    final_result.append(docs_links[2*doc_index])
                    final_result.append(docs_links[(2*doc_index) + 1])
                    count += 1

        return final_result
