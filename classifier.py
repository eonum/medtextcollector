import pickle
import os
from tokenizer import SimpleGermanTokenizer
import vectorizer

class Classifier:
    def __init__(self, config):
        self.config = config
        self.model = self.load_model_from_file()
        self.tokenizer = SimpleGermanTokenizer()
    
    def load_model_from_file(self):
        with open(os.path.join(self.config['base-folder'], 'classificator','naive_bayes_model.pickle'), 'rb') as file:
            return pickle.load(file)
            
    def classify(self, document):
        return self.model.prob_classify(vectorizer.bag_of_words(self.tokenizer.tokenize(document))).prob(True)
    