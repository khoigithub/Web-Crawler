import math
import os

page_rank_dict = {}
url_to_id_mapping = {}
id_to_url_mapping = {}

def get_outgoing_links(URL):
    if len(url_to_id_mapping) == 0:
        create_mapping_dict()
    if URL not in url_to_id_mapping:
        return None
    id = url_to_id_mapping[URL]

    URL_list = []
    
    filein = open(os.path.join(os.getcwd(), 'data', str(id), "outgoing_links.txt"), 'r')

    for line in filein:
        line = line.strip()
        URL_list.append(line)
    return URL_list

def get_incoming_links(URL):
    if len(url_to_id_mapping) == 0:
        create_mapping_dict()
    if URL not in url_to_id_mapping:
        return None
    id = url_to_id_mapping[URL]

    links_from = []
    filein = open(os.path.join(os.getcwd(), 'data', str(id), "incoming_links.txt"), 'r')

    for line in filein:
        line = line.strip()
        links_from.append(line)

    return links_from

def get_tf(URL, word):
    if len(url_to_id_mapping) == 0:
        create_mapping_dict()
    if URL not in url_to_id_mapping:
        return 0
    id = url_to_id_mapping[URL]

    filein = open(os.path.join(os.getcwd(), 'data', str(id), "tf.txt"), 'r')

    fruit = filein.readline().strip()
    while fruit != '':
        tf = float(filein.readline().strip())
        if fruit == word and tf != None:
            return tf
        fruit = filein.readline().strip()
    return 0

def get_idf(word):

    filein = open(os.path.join(os.getcwd(), 'data', "idf.txt"), 'r')

    total_fruit = 0
    total_docs = 0
    fruit = filein.readline().strip()
    while fruit != '':
        num_fruit = int(filein.readline().strip())
        if fruit == word:
            total_fruit = num_fruit
        if fruit == 'total':
            total_docs = num_fruit
        fruit = filein.readline().strip()

    if total_fruit == 0:
        return 0
    value = total_docs/(1 + total_fruit)
    idf = math.log(value, 2)

    return idf

def get_tf_idf(URL, word):
    tf_idf = math.log(1 + get_tf(URL, word), 2) * get_idf(word)

    return tf_idf

def get_page_rank(URL):
    if len(url_to_id_mapping) == 0:
        create_mapping_dict()
    if URL not in url_to_id_mapping:
        return -1
    if len(page_rank_dict) == 0:
        filein = open(os.path.join(os.getcwd(), 'data', "all-page-rank.txt"), 'r')
        count_id = 0
        for line in filein:
            line = line.strip()
            page_rank_dict[id_to_url_mapping[count_id]] = line
            count_id += 1
        return float(page_rank_dict[URL])
    else:
        return float(page_rank_dict[URL])

#mapping function that create a dictionary with all of the url to id and id to url mapping
def create_mapping_dict():
    file_link = open(os.path.join(os.getcwd(), 'data', 'url-and-id-mapping.txt'))
    link = file_link.readline().strip()
    while link != '':
        id = int(file_link.readline().strip())
        id_to_url_mapping[id] = link
        url_to_id_mapping[link] = id
        link = file_link.readline().strip()






    





