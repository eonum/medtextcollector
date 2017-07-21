import os
import tldextract

def extract_urls(path):
    urls = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames: 
            with open(os.path.join(dirpath, filename), 'r') as file:
                header = file.readline()
                url = header.split(';')[0].strip('"')
                urls.append(url)
        break # no subdirectories
    return urls            
                
def extract_tlds(path):
    urls = extract_urls(path)
    tlds = set()
    for url in urls:    
        tld = tldextract.extract(url)
        tld = tld.domain + '.' + tld.suffix
        tlds.add(tld)
    return tlds
    