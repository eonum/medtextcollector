from load_config import __CONFIG__
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import justext
import os
import re
from unidecode import unidecode
from hashlib import md5
from readability import Document
from lxml import html
import random
from operator import itemgetter
import atexit
import json
import sys
from classifier import Classifier

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        if not self.load_state():
            self.urls = [(base_url, 1)]
            self.visited_urls = []
            self.content_hashes = []
        
        if not os.path.exists(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages')):
            os.makedirs(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages'))
        
        self.classifier = Classifier(__CONFIG__)
        
        atexit.register(self.save_state)
            
    def save_state(self):
        self.sort_and_crop_urls()
        state = {'visited_urls': self.visited_urls, 'urls': self.urls, 'content_hashes': self.content_hashes}
        with open(os.path.join(__CONFIG__['base-folder'], 'crawler', 'crawler_state.json'), "w") as file:
            json.dump(state, file)
        print("Current state was saved to filesystem.")
        
    def load_state(self):
        try:
            with open(os.path.join(__CONFIG__['base-folder'], 'crawler', 'crawler_state.json'), "r") as file:
                print("Loading crawler state from filesystem ...")
                state = json.load(file)
                self.urls = state['urls']
                self.visited_urls = state['visited_urls']
                self.content_hashes = state['content_hashes']
                return True
        except FileNotFoundError:
            return False
            
    def sort_and_crop_urls(self):
        self.urls.sort(key=itemgetter(1), reverse=True)
        
        if __CONFIG__['max_urls'] > 0:
            if len(self.urls) > __CONFIG__['max_urls']:
                self.urls = self.urls[:__CONFIG__['max_urls']]
    
    def add_visited_url(self, url):
        self.visited_urls.append(url)
            
    def get_next_url(self):
        if len(self.urls) == 0:
            return None
        self.sort_and_crop_urls()
        url = self.urls.pop(0)
        self.add_visited_url(url[0])
        return url[0]
    
    def add_url(self, url):
        if url in self.visited_urls:
            return False
        
        try:
            next(x for x in self.urls if x[0] == url)
        except StopIteration:
            p = self.get_p(url)
            if p > __CONFIG__['threshold']:
                self.urls.append((url, p))
            return True
        
        return False

    def get_p(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        
        if not soup.find():
            return
        
        if len(r.content) > 0:
            content = self.extract_content(r.content)
        
        p = self.classifier.classify(content)
        
        print(" Rating "+ url + " :" + str(p))
        
        return p
        
    def is_absolute_url(self, url):
        return bool(urlparse(url).netloc)
    
    def get_absolute_url(self, current_url, next_url):
        if not self.is_absolute_url(next_url):
            next_url = urljoin(current_url, next_url)
        return next_url
    
    def scheme_is_http_or_none(self, url):
        scheme = urlparse(url).scheme
        return scheme == 'http' or scheme == ''
    
    def slugify(self, s):
        return re.sub(r'\W+', '-', unidecode(s).lower())
    
    def filename_from_url(self, url):
        slug = self.slugify(url) + '.txt'
        max_size = os.statvfs(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages')).f_namemax
        if len(slug) > max_size:
            h = '_md5_'+str(md5(slug.encode('utf-8')).hexdigest()) + '.txt'
            return slug[:max_size-len(h)] + h
        return slug
 
    def extract_content_using_justext(self, raw_page):
        paragraphs = justext.justext(raw_page, justext.get_stoplist("German"))
        content = ''
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                if len(content) > 0:
                    content += '\n'
                content += paragraph.text    
        return content   
     
    def extract_content_using_readability(self, raw_page):
        doc = Document(raw_page)    
        html_doc = html.document_fromstring(doc.summary())
        return html_doc.text_content()
    
    def extract_content(self, raw_page):
        if __CONFIG__['boilerplate-removal'] == 'justext':
            return self.extract_content_using_justext(raw_page)
        elif __CONFIG__['boilerplate-removal'] == 'readability':
            return self.extract_content_using_readability(raw_page)
        
    def content_is_duplicated(self, content):       
        h = md5(content.encode('utf-8')).hexdigest()
        if h in self.content_hashes:
            return True
        self.content_hashes.append(h)
        return False
    
    def process_url(self, url):
        print('Processing ' + url + ' ...')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        
        if not soup.find():
            return
        
        if len(r.content) > 0:
            content = self.extract_content(r.content)
        
        if self.content_is_duplicated(content):
            return
        
        if len(content) > 0:               
            with open(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages', self.filename_from_url(url)), 'w') as file:       
                file.write(content)
            
        for a in soup.find_all('a'):
            if self.scheme_is_http_or_none(a.get('href')):
                self.add_url(self.get_absolute_url(url, a.get('href')))
    
    def crawl(self):
        url = self.get_next_url()
        while url:
            try:
                self.process_url(url)
                url = self.get_next_url()
            except KeyboardInterrupt:
                sys.exit()
                

if __name__ == '__main__':
    crawler = Crawler(__CONFIG__['crawler-root-url'])
    crawler.crawl()
