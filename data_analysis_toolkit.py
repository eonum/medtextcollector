import os
import random
from tokenizer import SimpleGermanTokenizer
from tqdm import tqdm
from operator import itemgetter

# TODO: can probably be deleted or should be replaced with nltk.FreqDist
def get_token_frequencies(directory):
    tokenizer = SimpleGermanTokenizer()
    token_frequencies = {}
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in tqdm(filenames): 
            with open(os.path.join(dirpath, filename), 'r') as file:
                tokens = tokenizer.tokenize(file.read())
                for t in tokens:
                    if t in token_frequencies:
                        token_frequencies[t] += 1
                    else:
                        token_frequencies[t] = 1
    return token_frequencies

# TODO: can probably be deleted or should be replaced with nltk.FreqDist
def get_sorted_tokens(directory, n=None):
    token_frequencies = get_token_frequencies(directory)
    return sorted(token_frequencies.items(), key=itemgetter(1), reverse=True)[:n]

def load_documents(file_names):
    documents = []
    load_errors = []
    for filename in file_names: 
        with open(filename, 'r') as file:
            try:
                documents.append(file.read())
            except UnicodeDecodeError:
                load_errors.append(filename)
    random.shuffle(documents)
    return documents, load_errors

def get_files_from_folder(path):
    file_names = []
    for (dirpath, dirnames, subfilenames) in os.walk(path):
        for filename in subfilenames: 
            file_names.append((os.path.join(dirpath, filename)))
    return file_names

def extract_sentences(content, sentence_detector):
    return [sentence.replace('\n', ' ') for sentence in sentence_detector.tokenize(content) if not sentence.isspace()]
