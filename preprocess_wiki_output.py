import argparse
import os
from hashlib import md5

def split_file_to_documents(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        documents = content.split('["')
        documents = [document[:-2] for document in documents]
        return documents
    
def clean_document(document):
    unwanted_chars= ['[', ']', '(', ')', '&', '/', '-', '<', '>', '|', '*', '!', ':']
    clean_document = ''
    for c in document:
        if not c in unwanted_chars:
            clean_document += c
        else:
            clean_document += ' '
        
    return clean_document

def generate_output_filename(document):
    h = md5(document.encode('utf-8')).hexdigest()
    return 'wiki_' + h + '.txt'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocesses the output of the wiki scripts for medtextcollector_pipeline.py. Has to be executed for each category of samples individually.')
    parser.add_argument('output_directory', help='Split and preprocessed documents are saved to this directory.')
    parser.add_argument('files', metavar='file', nargs='+', help='file which belongs to a category (e.g. clean_extract1)')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.output_directory):
        parser.error('The output directory does not exist.')
    
    for file in args.files:
        if not os.path.isfile(file):
            parser.error('%s does not exist.' % file)
    
    print("Processing files ...")
    documents = []
    for file in args.files:
            for document in split_file_to_documents(file):
                documents.append(clean_document(document))
    
    print("Writing files ...")
    for document in documents:
        filename = generate_output_filename(document)
        with open(os.path.join(args.output_directory, filename), 'w') as file:
            file.write(document)


