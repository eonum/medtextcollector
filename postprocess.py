import os
import tldextract
import shutil

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


def extract_tld(url):
    tld = tldextract.extract(url)
    tld = tld.domain + '.' + tld.suffix
    return tld


def extract_tlds(path):
    return {extract_tld(url) for url in extract_urls(path)}
    

def extract_documents_by_tlds(tlds, input_path, output_path):
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for filename in filenames: 
            with open(os.path.join(input_path, filename), 'r') as file:
                header = file.readline()
                url = header.split(';')[0].strip('"')
                if extract_tld(url) in tlds:
                    print('Copying ' + filename)
                    shutil.copy2(os.path.join(dirpath, filename), output_path)
        break # no subdirectories
    

