import pickle
import os
import langdetect
from load_config import __CONFIG__

class Classifier:
    def __init__(self, config, validity_checks=True):
        self.config = config
        self.model = self.load_model_from_file()
        self.language = 'de' # unconfigurable for now
        self.validity_checks = validity_checks
    
    def load_model_from_file(self):
        with open(os.path.join(self.config['base-folder'], 'classificator', self.config['classifier-name'] + '.pickle'), 'rb') as file:
            return pickle.load(file)
            
    def classify(self, document):
        if self.validity_checks:
            if not valid_document(document):
                return 0.0
            try:
                if langdetect.detect(document) != self.language:
                    return 0.0
            except langdetect.lang_detect_exception.LangDetectException:
                return 0.0
        
        p = self.model.predict_proba([document])[0][0]
        p = 1 - p if __CONFIG__['invert-p'] else p
        return p
            
def valid_document(doc):
    return len(doc) >= __CONFIG__['doc-min-tokens']