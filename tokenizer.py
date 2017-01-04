import re
from nltk.stem.snowball import GermanStemmer
from nltk.corpus import stopwords

class SimpleTokenizer():
    def split_to_words(self, s, delimiter=' '):
        s = re.sub(r'[^\w\s]','',s)
        return s.split(delimiter)

class SimpleGermanTokenizer(SimpleTokenizer):    
    def tokenize(self, s):
        words = self.split_to_words(s)
        stemmed_words = self.stem_words(words)
        return stemmed_words
        
    def stem_words(self, words):
        stemmer = GermanStemmer()
        stemmed_words = []        
        for word in words:
            stemmed_words.append(stemmer.stem(word))
        return stemmed_words  
    