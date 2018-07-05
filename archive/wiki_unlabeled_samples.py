from load_config import __CONFIG__
import wikipedia
from hashlib import md5
import os


if __name__ == '__main__':
    wikipedia.set_lang('de')
    while True:
        if not os.path.exists(os.path.join(__CONFIG__['input-folder'], 'unlabeled')):
            os.makedirs(os.path.join(__CONFIG__['input-folder'], 'unlabeled'))
        
        print("Loading unlabeled sample from wikipedia ...")
        
        try:
            content = wikipedia.page(wikipedia.random()).content
        except wikipedia.exceptions.DisambiguationError:
            continue
        except wikipedia.exceptions.PageError:
            continue
        
        cleaned_content = ''
        for line in content.split('\n'):
            if '== Siehe auch ==' in line:
                break
            if '== Literatur ==' in line:
                break
            if '== Weblinks ==' in line:
                break
            line = line.replace('=', '')
            cleaned_content += line + '\n'
                   
        h = md5(cleaned_content.encode('utf-8')).hexdigest()
        
        with open(os.path.join(__CONFIG__['input-folder'], 'unlabeled', h + '.txt'), 'w') as file:       
            file.write(cleaned_content)