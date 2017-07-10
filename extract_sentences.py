import nltk
import os
from optparse import OptionParser
from tqdm import tqdm


# not used so far
# idea from https://github.com/devmount/GermanWordEmbeddings/blob/master/preprocessing.py
def extract_sentences(s):
    # sentence detector
    sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')
    sentences = sentence_detector.tokenize(s)

    return sentences


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", help="specify input folder")
    parser.add_option("-o", "--output", dest="output", help="specify output file")
    
    (options, args) = parser.parse_args()
    
    print("Sentence Extractor")
    
    if not options.input:
        parser.error("Specify an input folder.")
    
    if not options.output:
        parser.error("Specify an output file.")
        
    if not os.path.exists(options.input):
        parser.error("Input path doesn't exist.")
        
    print("Input: " + options.input)
    print("Output: " + options.output)
    
    with open(options.output, 'w') as out_file:
        for (dirpath, dirnames, filenames) in os.walk(options.input):
            for filename in tqdm(filenames): 
                with open(os.path.join(dirpath, filename), 'r') as file:
                    header = file.readline()
                    content = file.read()
                    sentences = extract_sentences(content)
                    for sentence in sentences:
                        print(sentence, file=out_file)
            break
         
                                                            
