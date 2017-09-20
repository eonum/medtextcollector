import argparse
import os
from hashlib import md5
import re


def split_buf_to_documents(buf, output_directory):
    open_index = -1
    close_index = -1
    while(True):
        open_index = buf.find('["')
        if open_index < 0:
            return buf
        close_index = buf.find('"]')
        if close_index < 0:
            return buf
        document = buf[open_index+2:close_index]
        clean_and_save_document(document, output_directory)
        buf = buf[close_index+2:]
    return buf

        
def split_file_to_documents(file_path, output_directory):
    with open(file_path, 'r') as file:
        buf = ''
        while True:
            data = file.read(1024)
            if not data:
                break
            buf += data
            buf = split_buf_to_documents(buf, output_directory)                   


def clean_and_save_document(document, output_directory):
    document = remove_picture_annotations(document)
    document = remove_title(document)
    #document = remove_wiki_links(document)
    document = remove_newlines(document)

    # replace all multiple whitespaces with a single one
    document = re.sub( '\s+', ' ', document).strip()

    #document = clean_document(document)
    filename = generate_output_filename(document)
    with open(os.path.join(output_directory, filename), 'w') as file:
        file.write(document)

def remove_picture_annotations(document):
    # remove picture annotations of the form "\nDatei: ... \n in wiki dumps"
    re.DOTALL = True
    document = re.sub('\\\\nDatei:(.+?)\\\\n', ' ', document)
    document = re.sub('>Datei:(.+?)\\\\n', ' ', document)
    document = re.sub('> Datei:(.+?)\\\\n', ' ', document)

    return document


def remove_title(document):
    # remove title annotations from wiki dumps
    return re.sub('<!--(.+?)-->', " " + r'\1' + " ", document)


def remove_newlines(document):
    document = re.sub('\n', ' ', document)
    document = re.sub('\\n', ' ', document)
    document = re.sub('\\\\n', ' ', document)

    return document


# def remove_wiki_links(document):
#     itr = re.finditer('\[\[(.*?)\]\]', document)
#     doc = []
#     left = 0
#     right = 0
#     for match in itr:
#         span = match.span()
#         text = match.group()
#
#         if '|' in text:
#             replacement = text.split('|')[1]
#             right = span[0]
#             doc.append(document[left:right] + replacement)
#             left = span[1]
#
#     doc.append(document[left:])
#
#     output = "".join(doc)
#     output = re.sub('\[\[', ' ', output)
#     output = re.sub('\]\]', ' ', output)
#
#     return output




def clean_document(document):
    unwanted_chars= ['[', ']', '(', ')', '&', '/', '-', '<', '>', '|', '*', '!', ':', '']
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
    for file in args.files:
        split_file_to_documents(file, args.output_directory)
    