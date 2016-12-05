import pickle
import os
from tokenizer import SimpleGermanTokenizer
import vectorizer
class Classifier:
    def __init__(self, config):
        self.config = config
        self.model = self.load_pos_naive_bayes_model_from_file()
        self.tokenizer = SimpleGermanTokenizer()
    
    def load_modelfrom_file(self):
        with open(os.path.join(self.config['base-folder'], 'classificator','pos_naive_bayes_model.pickle'), 'rb') as file:
            pickle.load(file)
            
    def classify(self, document):
        return self.model.prob_classify(vectorizer.simple_bag_of_words(self.tokenizer.tokenize(document))).prob(True)
    