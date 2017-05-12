import os
from pprint import pprint
from tokenizer import SimpleGermanTokenizer

def get_empty_files(directory):
    empty_files = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames: 
            with open(os.path.join(dirpath, filename), 'r') as file:
                if len(file.read()) == 0:
                    empty_files.append(os.path.join(dirpath, filename))
    return empty_files


def print_empty_files(directory):    
    print('Êmpty files in directory: ')
    for empty_file in get_empty_files(directory):
        print(empty_file)
    

def remove_empty_files(directory):
    print('Removing empty files in directory %s. Press ENTER to continue. ' %directory)
    input()
    for empty_file in get_empty_files(directory):
        print(empty_file)
        os.system("rm %s" % empty_file)

        
def get_tokenless_documents(directory):
    tokenizer = SimpleGermanTokenizer()
    tokenless_documents = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames: 
            with open(os.path.join(dirpath, filename), 'r') as file:
                tokens = tokenizer.tokenize(file.read())
                token_count = len(tokens)
                if token_count < 10:
                    print("%s: " % filename)
                    pprint(tokens)
                if token_count == 0:
                    tokenless_documents.append(os.path.join(dirpath, filename))
    return tokenless_documents

                
def print_tokenless_documents(directory):
    print('Tokenless documents in directory: ')
    for tokenless_document in get_tokenless_documents(directory):
        print(tokenless_document)


def remove_tokenless_documents(directory): 
    pass