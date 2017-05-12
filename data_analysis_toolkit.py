import os
from tokenizer import SimpleGermanTokenizer
from tqdm import tqdm
from operator import itemgetter

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

def get_sorted_tokens(directory, n=None):
    token_frequencies = get_token_frequencies(directory)
    return sorted(token_frequencies.items(), key=itemgetter(1), reverse=True)[:n]