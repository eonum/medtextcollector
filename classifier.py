import pickle
import os
import vectorizer
import langdetect
from tokenizer import SimpleGermanTokenizer
from load_config import __CONFIG__

class Classifier:
    def __init__(self, config):
        self.config = config
        self.model = self.load_model_from_file()
        self.tokenizer = SimpleGermanTokenizer() # unconfigurable for now
        self.language = 'de' # unconfigurable for now
    
    def load_model_from_file(self):
        with open(os.path.join(self.config['base-folder'], 'classificator', self.config['classifier-name'] + '.pickle'), 'rb') as file:
            return pickle.load(file)
            
    def classify(self, document):
        if not valid_document(document):
            return 0.0
        if langdetect.detect(document) != self.language:
            return 0.0
        
        return self.model.prob_classify(vectorizer.bag_of_words(self.tokenizer.tokenize(document))).prob(True)

def valid_document(doc):
    return len(doc) >= __CONFIG__['doc-min-tokens']