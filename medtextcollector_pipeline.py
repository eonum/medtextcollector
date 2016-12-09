from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from vectorizer import simple_bag_of_words
from sklearn.feature_extraction.text import CountVectorizer
from nltk.classify.positivenaivebayes import PositiveNaiveBayesClassifier
from pprint import pprint
import os
import pickle
import random


def load_documents(path):
    documents = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames: 
            with open(os.path.join(dirpath, filename), 'r') as file:
                documents.append(file.read())
        break
    random.shuffle(documents)
    testset_len = int(len(documents) * __CONFIG__['testset-ratio'])
       
    return documents[testset_len:], documents[:testset_len]


def evaluate(model, positive_vectorized_documents_test, negative_vectorized_documents_test):
    pos_pos = 0
    pos_neg = 0
    neg_neg = 0
    neg_pos = 0
    
    t = __CONFIG__['threshold']
    
    for document in positive_vectorized_documents_test:
        p = model.prob_classify(document).prob(True)
        if p >= t:
            pos_pos += 1
        else:
            pos_neg += 1

    for document in negative_vectorized_documents_test:
        p = model.prob_classify(document).prob(True)
        if p >= t:
            neg_pos += 1
        else:
            neg_neg += 1
    
    acc = pos_pos / (pos_pos + pos_neg + neg_neg + neg_pos)
    prec = pos_pos / (pos_pos + pos_neg)
    rec = pos_pos / (pos_pos + pos_neg)
    return acc, prec, rec


def unskew(dataset_a, dataset_b):
    min_len = min(len(dataset_a), len(dataset_b))
    return dataset_a[:min_len], dataset_b[:min_len
                                          
                                          ]
def run():
    print('Preparing base folder... ')
    if not os.path.exists(os.path.join(__CONFIG__['base-folder'], 'classificator')):
        os.makedirs(os.path.join(__CONFIG__['base-folder'], 'classificator'))
        
    print('Loading data ...')
    positive_documents_train, positive_documents_test = load_documents(os.path.join(__CONFIG__['input-folder'], 'positive'))
    unlabeled_documents_train, unlabeled_documents_test = load_documents(os.path.join(__CONFIG__['input-folder'], 'unlabeled'))
    
    positive_documents_train, unlabeled_documents_train = unskew(positive_documents_train, unlabeled_documents_train)
    positive_documents_test, unlabeled_documents_test = unskew(positive_documents_test, unlabeled_documents_test)
    
    print("Training")
    print('Tokenizing training set ...')
    tokenizer = SimpleGermanTokenizer()
    positive_tokenized_documents_train = []
    unlabeled_tokenized_documents_train = []
    for document in positive_documents_train:
        positive_tokenized_documents_train.append(tokenizer.tokenize(document))
    for document in unlabeled_documents_train:
        unlabeled_tokenized_documents_train.append(tokenizer.tokenize(document))
    
    print('Vectorizing training set ...')
    positive_vectorized_documents_train = [simple_bag_of_words(tokens) for tokens in positive_tokenized_documents_train]
    unlabeled_vectorized_documents_train = [simple_bag_of_words(tokens) for tokens in unlabeled_tokenized_documents_train]
    
    classifier = PositiveNaiveBayesClassifier.train(positive_vectorized_documents_train, unlabeled_vectorized_documents_train)
    
    print("Saving model to " + os.path.join(__CONFIG__['base-folder'], 'classificator', 'pos_naive_bayes_model.pickle') + " ...")    
    with open(os.path.join(__CONFIG__['base-folder'], 'classificator','pos_naive_bayes_model.pickle'), 'wb') as file:
        pickle.dump(classifier, file)
      
    print("Evaluation")  
    print('Tokenizing test set...')
    positive_tokenized_documents_test = []
    unlabeled_tokenized_documents_test = []
    for document in positive_documents_test:
        positive_tokenized_documents_test.append(tokenizer.tokenize(document))
    for document in unlabeled_documents_test:
        unlabeled_tokenized_documents_test.append(tokenizer.tokenize(document))

    print('Vectorizing test set ...')
    positive_vectorized_documents_test = [simple_bag_of_words(tokens) for tokens in positive_tokenized_documents_test]
    unlabeled_vectorized_documents_test = [simple_bag_of_words(tokens) for tokens in unlabeled_tokenized_documents_test]

    acc, prec, rec = evaluate(classifier, positive_vectorized_documents_test, unlabeled_vectorized_documents_test)
    
    print("Accuracy:  " + str(acc))
    print("Precision: " + str(prec))
    print("Recall:    " + str(rec))

if __name__ == '__main__':
    run()