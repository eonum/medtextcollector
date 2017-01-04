from crawler import Crawler

class MSDManualCrawler(Crawler):
    def get_p(self, url):
        if 'msdmanual.pl' in url:
            return 1
        return 0

    def filename_from_url(self, url):
        return url.split('m=')[1] +'.txt'
 
    
if __name__ == '__main__':
    crawler = MSDManualCrawler('http://www.msd-manual.de/msdmanual/htbin/msdmanual.pl?m=0-0')
    crawler.crawl()