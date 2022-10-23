import math
import searchdata
import os
import time

id_to_url_mapping = {}
url_to_id_mapping = {}
vector_for_all_docs_dict = {}

def search(phrase, boost):
    if len(id_to_url_mapping) == 0:
        create_mapping_dict()
    if len(vector_for_all_docs_dict) == 0:
        all_vectors_for_docs()

    dictionary_word = {}                     #{apple: 2, peach: 1}
    vector_to_docs_query_temp = []           #[[apple/doc1, apple/doc2...], [peach/doc1, peach/doc2]]
    vector_to_docs_query = []                #[[apple/doc1, peach/doc1...], [apple/doc2, peach/doc2]]
    cosine_sim_list = []
    boosted_dict = {}
    temp_final_result = []
    final_result = []

    words = phrase.split(' ')

    #add all words in the query into the dictionary
    for word in words:
        if word not in dictionary_word:
            dictionary_word[word] = 0
        dictionary_word[word] += 1
    
    #get the vector for all of the specific words, see the comment of vector_docs_list to know how the list is structure
    for word in dictionary_word:
        if word in vector_for_all_docs_dict:
            vector_to_docs_query_temp.append(vector_for_all_docs_dict[word])
        else:
            vector_to_docs_query_temp.append([0.0 for i in range(len(url_to_id_mapping))])      

    vector_to_docs_query = [[] for i in range(len(url_to_id_mapping))]

    for i in range(len(url_to_id_mapping)):
        for j in range(len(vector_to_docs_query_temp)):
            vector_to_docs_query[i].append(vector_to_docs_query_temp[j][i])
            
    #create the vector for the query and calculate the left denomination
    vector_query = query_vector(dictionary_word, words)
    left_denom = left_denom_calculate(vector_query)

    #calculate the cosine similarity
    for i in range(len(vector_to_docs_query)):
        numerator = 0
        right_denom = 0
        for j in range(len(vector_query)):
            numerator += vector_query[j] * vector_to_docs_query[i][j]
            right_denom += vector_to_docs_query[i][j] * vector_to_docs_query[i][j]
        right_denom = math.sqrt(right_denom)
        denom = right_denom * left_denom
        if denom != 0:
            cosine = numerator/denom
        else:
            cosine = 0
        cosine_sim_list.append(cosine)

    #calculate and sort the list    
    for i in range(len(cosine_sim_list)):
        url = id_to_url_mapping[i]
        if boost:
            boosted_dict[url] = searchdata.get_page_rank(url) * cosine_sim_list[i]
        else:
            boosted_dict[url] = cosine_sim_list[i]

    boosted_dict = dict(sorted(boosted_dict.items(), key = get_value, reverse = True))
    
    #put the result in the final dictionary and return the top 10
    for key in boosted_dict:
        temp_dict = {}
        temp_dict['url'] = key
        temp_dict['title'] = page_title(key)
        temp_dict['score'] = boosted_dict[key] 
        temp_final_result.append(temp_dict)

    if len(temp_final_result) <= 10:
        return temp_final_result
    else:
        for i in range(10):
            final_result.append(temp_final_result[i])
        return final_result

def all_vectors_for_docs():
    filein = open(os.path.join(os.getcwd(), 'data', "idf.txt"), 'r')

    fruit = filein.readline().strip()
    while fruit != '':
        num_fruit = int(filein.readline().strip())
        if fruit not in vector_for_all_docs_dict:
            vector_for_all_docs_dict[fruit] = []
        fruit = filein.readline().strip()
    
    for item in vector_for_all_docs_dict:
        for link in url_to_id_mapping:
            vector_for_all_docs_dict[item].append(searchdata.get_tf_idf(link, item))

def query_vector(dict, words):
    vector = []
    for word in dict:
        idf = searchdata.get_idf(word)
        vector.append(math.log(1 + int(dict[word])/len(words), 2) * idf)
    
    return vector

def left_denom_calculate(list):
    denom = 0
    for i in range(len(list)):
        denom += list[i] * list[i]
    denom = math.sqrt(denom)
    
    return denom

def page_title(link):
    title = link.split('/')[5].strip('.html')
    return title

def get_value(item):
    return item[1]

def create_mapping_dict():
    file_link = open(os.path.join(os.getcwd(), 'data', "url-and-id-mapping.txt"), 'r')
    link = file_link.readline().strip()
    while link != '':
        id = int(file_link.readline().strip())
        id_to_url_mapping[id] = link
        url_to_id_mapping[link] = id
        link = file_link.readline().strip()

# start = time.time()
# search('**PHRASE YOU WANT TO SEARCH FOR**', True)
# end = time.time()
# print(end - start)