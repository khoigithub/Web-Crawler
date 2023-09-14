import webdev
import os_management
import sys

#test github branch

visited_links = []          #all of the link that has already visited
links_to_visit = []         #all of the links need to be visit
url_and_id_dict = {}         #mapping url to an id
idf = {}

sys.setrecursionlimit(1100)

def crawl(seed):
    if os_management.check_directory('data'):
        if not os_management.check_file('./data', 'flag.txt'):
            os_management.reset_everything('data')
    
    contents = webdev.read_url(seed)
    mystring = ''
    outgoing_links = []     #list with all of the outgoing links for each crawl
    incoming_links = {}
    tf_temp = {}            
    tf = {}                 #dict with term frequency for each word with key is the word
    

    for i in range(len(contents)):
        mystring += contents[i]

#get the title
    title = page_title(mystring)

    if seed not in url_and_id_dict:
        url_and_id_dict[seed] = len(url_and_id_dict)

    tags = mystring.split('"')
    for i in range(len(tags)):
        if i % 2 == 1:
            full = full_url(tags[i], seed)
            links_to_visit.append(full)
            outgoing_links.append(full)

#tf and idf dictionary
    count_total = 0
    for word in paragraph(mystring).split('\n'):
        if word not in tf_temp:
            tf_temp[word] = 0
        tf_temp[word] += 1
        count_total += 1
    tf_temp['total'] = count_total

    for key in tf_temp:
        if key != 'total':
            tf[key] = tf_temp[key]/tf_temp['total']
        if key in idf:
            idf[key] += 1
        elif key not in idf:
            idf[key] = 1

#Check if the link has already been visited
    if seed not in visited_links:
        visited_links.append(seed)
        if not os_management.check_directory('data'):
            os_management.create_directory('data')
        if not os_management.check_file('./data', 'flag.txt'):
            os_management.create_file('./data', 'flag.txt', '')
        if not os_management.check_directory('./data/' + str(url_and_id_dict[seed])):
            os_management.create_directory('./data/' + str(url_and_id_dict[seed]))
            
        # os_management.create_file('./data/paragraph', title + '-paragraph.txt', paragraph(mystring))

        os_management.create_file('./data/' + str(url_and_id_dict[seed]), 'tf.txt', dict_to_str(tf))
        os_management.create_file('./data/' + str(url_and_id_dict[seed]), 'outgoing_links.txt', '\n'.join(outgoing_links))

#if the link has not been visited, recursively called the crawl function again
    for i in range(len(links_to_visit)):
        if links_to_visit[i] not in visited_links:
            crawl(links_to_visit[i])

#Create a file with all of the title and create a flag to check if the program should delete everything
    # os_management.create_file('data', 'all_links.txt', '\n'.join(title_list))
    os_management.delete_file('./data', 'flag.txt')

    os_management.create_file('data', 'url-and-id-mapping.txt', dict_to_str(url_and_id_dict))
    os_management.create_file('data', 'idf.txt', dict_to_str(idf))

#takes in a string and combined it with the link from the seed
def full_url(str, seed):
    seed = seed.split('/')
    str = str.strip('.')
    full_link = seed[0] + '//' + seed[2] + '/' + seed[3] + '/' + seed[4] + str
    return full_link

def paragraph(str):
    paragraph = str.split('<p>')[1].split('</p>')[0].strip()
    return paragraph

def page_title(str):
    return str.split('</')[0].strip('<html><head><title>')

def dict_to_str(dict):
    converted_string = str(dict).strip("{ }").replace(', ','\n').replace("'", '').replace(": ", '\n')
    return converted_string

crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html')