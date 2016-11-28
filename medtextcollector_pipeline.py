from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from vectorizer import simple_bag_of_words
from sklearn.feature_extraction.text import CountVectorizer
from nltk.classify.positivenaivebayes import PositiveNaiveBayesClassifier
from pprint import pprint
import os
import pickle

if __name__ == '__main__':
    print('Preparing base folder... ')
    if not os.path.exists(__CONFIG__['base-folder']):
        os.makedirs(__CONFIG__['base-folder'])
        
    print('Loading data ...')
    positive_documents = ['Dies ist ein Testdokument.', 'Dies ist auch ein Testdkument.', 'Und noch ein Testdokument']
    unlabeled_documents = ['Lorem ipsum.', 'Dolor sit amet.', 'Blablaba bla bla.']
    
    print('Tokenizing ...')
    tokenizer = SimpleGermanTokenizer()
    positive_tokenized_documents = []
    unlabeled_tokenized_documents = []
    for document in positive_documents:
        positive_tokenized_documents.append(tokenizer.tokenize(document))
    for document in unlabeled_documents:
        unlabeled_tokenized_documents.append(tokenizer.tokenize(document))
    
    print('Vectorizing ...')
    positive_vectorized_documents = [simple_bag_of_words(tokens) for tokens in positive_tokenized_documents]
    unlabeled_vectorized_documents = [simple_bag_of_words(tokens) for tokens in unlabeled_tokenized_documents]
    
    classifier = PositiveNaiveBayesClassifier.train(positive_vectorized_documents, unlabeled_vectorized_documents)
    
    print("Saving model to " + os.path.join(__CONFIG__['base-folder'], 'pos_naive_bayes_model.pickle') + " ...")    
    with open(os.path.join(__CONFIG__['base-folder'], 'pos_naive_bayes_model.pickle'), 'wb') as file:
        pickle.dump(classifier, file)
        
    pprint(classifier.prob_classify(simple_bag_of_words(tokenizer.tokenize("Nochmal ein Testdokument."))).prob(True))    
