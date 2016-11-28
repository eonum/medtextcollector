from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.classify.positivenaivebayes import PositiveNaiveBayesClassifier
from pprint import pprint

def bag_of_words(words):
    return dict([(word, True) for word in words])

if __name__ == '__main__':
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
    positive_vectorized_documents = [bag_of_words(tokens) for tokens in positive_tokenized_documents]
    unlabeled_vectorized_documents = [bag_of_words(tokens) for tokens in unlabeled_tokenized_documents]
    
    if __CONFIG__['debug']:
        vocab = vectorizer.get_feature_names()
        print('Vocabulary: ')
        pprint(vocab)
    
    classifier = PositiveNaiveBayesClassifier.train(positive_vectorized_documents, unlabeled_vectorized_documents)
    
    pprint(classifier.prob_classify(bag_of_words(tokenizer.tokenize("Nochmal ein Testdokument."))).prob(True))    
    