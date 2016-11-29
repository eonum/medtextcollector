import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self):
        self.urls = ['http://www.msd-manual.de/msdmanual/']
    
    def get_next_url(self):
        if len(self.urls) == 0:
            return None
        return self.urls.pop(0)
    
    def run(self):
        next_url = self.get_next_url()
        while next_url:
            print('Processing ' + next_url + ' ...')
            r = requests.get(next_url)
            print(r.text)
            next_url = self.get_next_url()

if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()   