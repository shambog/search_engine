import os
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib import parse

#create the directory to put crawled files
def make_dir(dir_name):  
    
    print('Creating ' + '"'+ str(dir_name) + '"' + ' directory to keep crawled pages\n')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

#using HTMLParser to get the href tags and put those inside a set data structure
class Get_Linktag(HTMLParser):

    def __init__(self, page_url):
        self.page_url = page_url
        self.links = set()
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    newlink = parse.urljoin(self.page_url, value)
                    self.links.add(newlink)

    def ret_links(self):
        return self.links

#parsing the domain name to crawl pages from a single domain
def get_domain(url):
    
    try:
        parse_domain = urlparse(url).netloc.split('.')
        parsed_result = parse_domain[-2] + '.' + parse_domain[-1]
        return parsed_result
    except:
        return ''

#creating the Spider
def Spider(dir_name, curr_url, domain):
    
    FirstLink = curr_url
    make_dir(dir_name)
    to_be_crawled.add(FirstLink)
    page_crawl(curr_url)

#updating crawled and to_be_crawled lists
def page_crawl(curr_url):
    
    while len(to_be_crawled) > 0:
        if doc_count > 1500:        #we are crawling 1500 pages
            break
        curr_url = to_be_crawled.pop()
        
        if curr_url not in crawled_list:
            parsed_link = find_link(curr_url)
            fill_to_be_crawled(parsed_link)
            
            crawled_list.add(curr_url)
            print("Crawled Page Count :", len(crawled_list))
            print("Pages to be crawled :", len(to_be_crawled))
            print("The link to be crawled next : ", curr_url)

#decoding the html content and writing to a file
def find_link(new_url):
    
    content = ''
    try:
        resp = urlopen(new_url)
        if 'text/html' in resp.getheader('Content-Type'):
            content = resp.read()
            decoded_content = content.decode('utf-8')
        href_details = Get_Linktag(new_url)
        href_details.feed(decoded_content)
        write_file(decoded_content, dir_name, new_url)
    except:
        return set() #return empty 
    return href_details.ret_links()

#checking if the current url is in any of the Set data structure
def fill_to_be_crawled(links):
    
    for url in links:
        if (url in to_be_crawled) or (url in crawled_list):
            continue
        if (home_domain != get_domain(url)):  #crawl pages from a single domain
            continue
        to_be_crawled.add(url)

#writing html contents to a file
def write_file(html_content, dir_name, new_url):
    
    print('\nWriting to file ...\n')
    global doc_count
    doc_name = 'Doc-' + str(doc_count)
    doc_url_file(doc_name, new_url)
    myfile = dir_name + '/' + doc_name + '.html'
    doc_count = doc_count + 1
    with open(myfile, 'w', encoding='UTF-8') as f:
        f.write(html_content)
        f.close

#writing the document name and its url in a file
def doc_url_file(doc_name, new_url):
    
    myfile2 = 'doc_url_details.txt'
    if not os.path.isfile(myfile2):
        with open(myfile2, 'w', encoding='UTF-8') as f:
            f.write(doc_name + ' ' + new_url + '\n')
    else:
        with open(myfile2, 'a', encoding='UTF-8') as f:
            f.write(doc_name + ' ' + new_url + '\n')

def main():
    
    global home_domain
    global dir_name
    global doc_count
    global home_url
    global queue
    global to_be_crawled
    global crawled_list   
    dir_name = 'Crawled_Files'
    home_url = 'https://electronics.howstuffworks.com/tech'
    doc_count = 1

    to_be_crawled = set()       #declaring data structure
    crawled_list = set()
    home_domain = get_domain(home_url)
    
    Spider(dir_name, home_url, home_domain)
    print("\n\nExiting ...")

if __name__ == "__main__":
    main()

