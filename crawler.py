from load_config import __CONFIG__
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunsplit, urljoin
import justext
import os
import re
from unidecode import unidecode
from hashlib import md5

class Crawler:
    def __init__(self, base_url):
        self.urls = [base_url]
        self.visited_urls = []
        
        if not os.path.exists(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages')):
            os.makedirs(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages'))
    
    def get_next_url(self):
        if len(self.urls) == 0:
            return None
        url = self.urls.pop(0)
        self.visited_urls.append(url)
        return url
    
    def add_url(self, url):
        if url in self.visited_urls:
            return False
        
        self.urls.append(url)
        return True
    
    def is_absolute_url(self, url):
        return bool(urlparse(url).netloc)
    
    def get_absolute_url(self, current_url, next_url):
        if not self.is_absolute_url(next_url):
            split_url = urlparse(current_url)
            base_url = urlunsplit((split_url.scheme, split_url.netloc, '', '', ''))
            next_url = urljoin(base_url, next_url)
        return next_url
    
    def is_http(self, url):
        return urlparse(url).scheme == 'http'
    
    def slugify(self, s):
        return re.sub(r'\W+', '-', unidecode(s).lower())
    
    def filename_from_url(self, url):
        slug = self.slugify(url) + '.txt'
        max_size = os.statvfs(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages')).f_namemax
        if len(slug) > max_size:
            h = '_md5_'+str(md5(slug.encode('utf-8')).hexdigest()) + '.txt'
            return slug[:max_size-len(h)] + h
        return slug
    
    def run(self):
        url = self.get_next_url()
        while url:
            print('Processing ' + url + ' ...')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            
            paragraphs = justext.justext(r.content, justext.get_stoplist("German"))
            content = ''
            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    if len(content) > 0:
                        content += '\n'
                    content += paragraph.text
            
            if len(content) > 0:               
                with open(os.path.join(__CONFIG__['base-folder'], 'crawler', 'pages', self.filename_from_url(url)), 'w') as file:       
                    file.write(content)
                
            for a in soup.find_all('a'):
                if self.is_http(a.get('href')):
                    self.add_url(self.get_absolute_url(url, a.get('href')))
            
            url = self.get_next_url()


if __name__ == '__main__':
    crawler = Crawler(__CONFIG__['crawler-root-url'])
    crawler.run()   