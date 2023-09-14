import webdev
import os_management
import matmult
import os
import time

#The third comment test for github

def crawl(seed):
    if os_management.check_directory('data'):
        os_management.reset_everything('data')

    url_and_id_dict = {}            #mapping url to an id
    links_to_visit = []             #All of the links that needs to be visit
    visited_links = {}              #All of the links that has visit before
    idf_dict = {}
    outgoing_links_dict = {}
    incoming_links = {}

    links_to_visit.append(seed)

    while len(links_to_visit) != 0:
        tf_temp = {}            
        tf = {}                 #dict with term frequency for each word with key is the word
        outgoing_links = []     #all of the outgoing links of the page we are currently in
                       
        #Get the contents from the page
        contents = webdev.read_url(links_to_visit[0])
        mystring = ''

        #convert the content of the page to string
        for i in range(len(contents)):
            mystring += contents[i]

        #Get all of the outgoing links in the page we are in
        tags = mystring.split('href="')
        for i in range(1, len(tags)):
            full = full_url(tags[i].split('"')[0], seed)
            outgoing_links.append(full)
            outgoing_links_dict[links_to_visit[0]] = outgoing_links

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
            if key in idf_dict:
                idf_dict[key] += 1
            elif key not in idf_dict:
                idf_dict[key] = 1

        #for url mapping, if the link we are on is not in url_and_id_dict, we assign it to an id
        if links_to_visit[0] not in url_and_id_dict:
            url_and_id_dict[links_to_visit[0]] = len(url_and_id_dict)
    
        #Create all of the file we need
        if not os_management.check_directory('data'):
            os_management.create_directory('data')
        #Check and create the directory we need with id of the link is the name
        if not os_management.check_directory(os.path.join(os.getcwd(), 'data', str(url_and_id_dict[links_to_visit[0]]))):
            os_management.create_directory(os.path.join(os.getcwd(), 'data', str(url_and_id_dict[links_to_visit[0]])))
        os_management.create_file(os.path.join(os.getcwd(), 'data', str(url_and_id_dict[links_to_visit[0]])), 'outgoing_links.txt', '\n'.join(outgoing_links))
        # os_management.create_file(os.path.join(os.getcwd(), 'data', str(url_and_id_dict[links_to_visit[0]])), 'outgoing_links.txt', '\n'.join(outgoing_links))
        dict_to_file(tf, str(url_and_id_dict[links_to_visit[0]]), 'tf')
        

        #if the outgoing links of that page has not been visit before, add to the end of the queue
        for i in range(len(outgoing_links)):
            if outgoing_links[i] not in links_to_visit and outgoing_links[i] not in visited_links:
                links_to_visit.append(outgoing_links[i])
            if outgoing_links[i] not in incoming_links:
                incoming_links[outgoing_links[i]] = set([links_to_visit[0]])
            elif outgoing_links[i] in incoming_links:
                incoming_links[outgoing_links[i]].add(links_to_visit[0])

        #remove the first link of the links_to_visit list and continue the process
        remove_first = remove_from_queue(links_to_visit)
        visited_links[remove_first] = 1
    
    dict_to_file(idf_dict, 'idf', None)
    dict_to_file(url_and_id_dict, 'url-and-id-mapping', None)

    for link in incoming_links:
        os_management.create_file(os.path.join(os.getcwd(), 'data', str(url_and_id_dict[link])), 'incoming_links.txt', set_to_str(incoming_links[link]))
    page_rank_float = page_rank(url_and_id_dict, adjacency_matrix(url_and_id_dict, outgoing_links_dict))
    all_page_rank = []
    for item in page_rank_float:
        item = str(item)
        all_page_rank.append(item)
    os_management.create_file('data', 'all-page-rank.txt', '\n'.join(all_page_rank))

#takes in a string and combined it with the link from the seed
def full_url(str, seed):
    seed = seed.split('/')
    str = str.strip('.')
    full_link = seed[0] + '//' + seed[2] + '/' + seed[3] + '/' + seed[4] + str
    return full_link

def paragraph(str):
    paragraph = str.split('<p>')[1].split('</p>')[0].strip()
    return paragraph

def dict_to_str(dict):
    converted_string = str(dict).strip("{ }").replace(', ','\n').replace("'", '').replace(": ", '\n')
    return converted_string

def set_to_str(set):
    converted_set = str(set).strip('{ }').replace(', ','\n').replace("'", '')
    return converted_set

def dict_to_file(dict, filename1, filename2):
    if filename2 == None:
        fileout = open(os.path.join(os.getcwd(), 'data', filename1 + '.txt'), 'w')
    else:
        fileout = open(os.path.join(os.getcwd(), 'data', filename1, filename2 + '.txt'), 'w')
    for key in dict:
        fileout.write(key + '\n')
        fileout.write(str(dict[key]) + '\n')
    fileout.close()

def remove_from_queue(list):
    return list.pop(0)

def adjacency_matrix(url_and_id_dict, outgoing_links_dict):
    adjacency_matrix = []
    alpha = 0.1
    for i in url_and_id_dict:
        temp_list = [0 for i in range(len(url_and_id_dict))]
        count = 0
        for j in outgoing_links_dict[i]:
            temp_list[url_and_id_dict[j]] = 1
            count += 1
        for i in range(len(temp_list)):
            if temp_list[i] == 1:
                temp_list[i] = (1-alpha)/count
        for i in range(len(temp_list)):
            temp_list[i] += alpha/len(temp_list)
        adjacency_matrix.append(temp_list)

    return adjacency_matrix

def page_rank(url_and_id_dict, adjacency_matrix):

    start_percentage = 1/len(url_and_id_dict)
    t_prev = [[start_percentage for i in range(len(url_and_id_dict))]]
    t_next = matmult.mult_matrix(t_prev, adjacency_matrix)
    eu = matmult.euclidean_dist(t_prev, t_next)

    while eu > 0.0001:
        t_prev = t_next
        t_next = matmult.mult_matrix(t_prev, adjacency_matrix)
        eu = matmult.euclidean_dist(t_prev, t_next)
       
    return t_next[0]

# start = time.time()
# crawl('**LINK YOU WANT TO TEST WITH**')
# end = time.time()
# print(end - start)
