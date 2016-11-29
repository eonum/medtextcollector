import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunsplit, urljoin

class Crawler:
    def __init__(self):
        self.urls = ['http://www.msd-manual.de/msdmanual/']
        self.visited_urls = []
    
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
    
    def run(self):
        url = self.get_next_url()
        while url:
            print('Processing ' + url + ' ...')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            
            for a in soup.find_all('a'):
                if self.is_http(a.get('href')):
                    self.add_url(self.get_absolute_url(url, a.get('href')))
                
            url = self.get_next_url()

if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()   