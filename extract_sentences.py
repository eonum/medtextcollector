import nltk
import os
from optparse import OptionParser
from tqdm import tqdm


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", help="specify input folder")
    parser.add_option("-o", "--output", dest="output", help="specify output file")
    parser.add_option("-m", "--minwords", dest='minwords', type="int", default=None, help="specify minimal number of words per sentence")
    
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
    
    sentence_detector = nltk.data.load('tokenizers/punkt/german.pickle')
    with open(options.output, 'w') as out_file:
        for (dirpath, dirnames, filenames) in os.walk(options.input):
            for filename in tqdm(filenames[:10]): 
                with open(os.path.join(dirpath, filename), 'r') as file:
                    header = file.readline()
                    content = file.read()
                    sentences = sentence_detector.tokenize(content)
                    for sentence in sentences:
                        sentence = sentence.replace('\n', ' ')
                        split_sentence = sentence.split()
                        if not options.minwords or len(split_sentence) >= options.minwords:
                            sentence = ' '.join(sentence.split())
                            if not sentence.isspace():
                                print(sentence, file=out_file)
            break
         
                                                            
