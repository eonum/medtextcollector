from load_config import __CONFIG__
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import justext
import os
import re
from unidecode import unidecode
from hashlib import md5
from readability import Document, readability
from lxml import html
from operator import itemgetter
import atexit
import json
import sys
from classifier import Classifier
import tldextract
import time

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.request_cache = {}

        if not self.load_state():
            self.urls = [(base_url, 1)]
            self.visited_urls = []
            self.visits_per_tld = {}
            self.content_hashes = []
        
        if not os.path.exists(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages')):
            os.makedirs(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages'))
        
        self.classifier = Classifier(__CONFIG__)
        
        atexit.register(self.save_state)
            
    def save_state(self):
        self.sort_and_crop_urls()
        state = {'visited_urls': self.visited_urls, 'urls': self.urls, 'visits_per_tld': self.visits_per_tld, 'content_hashes': self.content_hashes}
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
                self.visits_per_tld = state['visits_per_tld']
                self.content_hashes = state['content_hashes']
                return True
        except FileNotFoundError:
            return False
            
    def sort_and_crop_urls(self):
        self.urls.sort(key=itemgetter(1), reverse=True)
        
        if __CONFIG__['max_urls'] > 0:
            if len(self.urls) > __CONFIG__['max_urls']:
                self.urls = self.urls[:__CONFIG__['max_urls']]
    
    def is_excluded_url(self, url):
        try: 
            next(x for x in __CONFIG__['excluded-urls'] if url.startswith(x)) 
        except StopIteration:
            return False
        return True
    
    def excluded_keyword_in_url(self, url):
        try: 
            ret = next(x for x in __CONFIG__['excluded-keywords-url'] if x in url) 
        except StopIteration:
            return False
        return bool(ret)
        
    
    def add_visited_url(self, url):
        self.visited_urls.append(url)
            
    def get_next_url(self):
        if len(self.urls) == 0:
            return None, None
        self.sort_and_crop_urls()
        while True:
            url = self.urls.pop(0)
            if not self.is_excluded_url(url[0]) and not self.excluded_keyword_in_url(url[0]):
                break
        
        self.add_visited_url(url[0])
        return url[0], url[1]
    
    def add_url(self, url):
        if self.is_excluded_url(url) or self.excluded_keyword_in_url(url):
            return False
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
        try:
            r = self.request_from_cache(url)
            if not r:
                return 0.0
        except Exception:
            return 0.0
        
        soup = BeautifulSoup(r.text, 'lxml')
        
        if not soup.find():
            return 0.0
        
        if len(r.content) > 0:
            content = self.extract_content(r.content)
        
        if not content:
            return 0.0
        
        p = self.classifier.classify(content)
        
        print(" Rating "+ url + " : " + str(p))
        
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
        try:
            doc = Document(raw_page)    
            html_doc = html.document_fromstring(doc.summary())
            return html_doc.text_content()
        except readability.Unparseable:
            print("Could not be parsed.")
            return None
    
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
    
    def request_from_cache(self, url):
        slug = self.slugify(url)
        if slug in self.request_cache:
            r = self.request_cache[slug]
        else:
            tld = tldextract.extract(url)
            tld = tld.domain + '.' + tld.suffix
            if not __CONFIG__['max-visits-per-tld'] == -1:
                if tld in self.visits_per_tld: 
                    if self.visits_per_tld[tld] >= __CONFIG__['max-visits-per-tld'] or __CONFIG__['max-visits-per-tld'] == 0:
                        print('Max. requests for %s reached.' % tld)
                        return None
                    else:
                        self.visits_per_tld[tld] += 1
                else:
                    self.visits_per_tld[tld] = 1
            r = requests.get(url)
            self.request_cache[slug] = r
        return r

    def process_url(self, url, p):
        print('Processing ' + url + ' ...')
        r = self.request_from_cache(url)
        
        if not r:
            return
        
        soup = BeautifulSoup(r.text, 'lxml')
        
        if not soup.find():
            return
        
        if len(r.content) > 0:
            content = self.extract_content(r.content)
            
        if not content:
            return
        
        if self.content_is_duplicated(content):
            print(' Duplicated content.')
            return
        
        if len(content) > 0:               
            with open(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages', self.filename_from_url(url)), 'w') as file:
                print(';'.join(['"%s"' % url, '"%s"' % time.strftime('%d-%m-%y-%H'), '"%s"' % __CONFIG__['classifier-name'], '"%s"'  % str(p)]), file=file)       
                file.write(content)
            
        for a in soup.find_all('a'):
            if self.scheme_is_http_or_none(a.get('href')):
                resulting_url = self.get_absolute_url(url, a.get('href'))
                if __CONFIG__['urldefrag']:
                    resulting_url = urldefrag(resulting_url)[0] 
                self.add_url(resulting_url)
    
    def crawl(self):
        url, p = self.get_next_url()
        while url:
            try:
                self.process_url(url, p)
                url, p = self.get_next_url()
            except KeyboardInterrupt:
                sys.exit()
        if not url:
            print("Nothing left to crawl. Bye bye.")
            
if __name__ == '__main__':
    crawler = Crawler(__CONFIG__['crawler-root-url'])
    crawler.crawl()
