from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from vectorizer import bag_of_words
from nltk import NaiveBayesClassifier
from nltk.metrics import accuracy, precision, recall, f_measure, ConfusionMatrix
from pprint import pprint
import os
import pickle
import random
import nltk

import pdb

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

def unskew(dataset_a, dataset_b):
    min_len = min(len(dataset_a), len(dataset_b))
    return dataset_a[:min_len], dataset_b[:min_len]

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
    positive_vectorized_documents_train = [(bag_of_words(tokens), True) for tokens in positive_tokenized_documents_train]
    unlabeled_vectorized_documents_train = [(bag_of_words(tokens), False) for tokens in unlabeled_tokenized_documents_train]
    
    classifier =  NaiveBayesClassifier.train(positive_vectorized_documents_train + unlabeled_vectorized_documents_train)
    
    print("Saving model to " + os.path.join(__CONFIG__['base-folder'], 'classificator', 'naive_bayes_model.pickle') + " ...")    
    with open(os.path.join(__CONFIG__['base-folder'], 'classificator','naive_bayes_model.pickle'), 'wb') as file:
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
    positive_vectorized_documents_test = [(bag_of_words(tokens), True) for tokens in positive_tokenized_documents_test]
    unlabeled_vectorized_documents_test = [(bag_of_words(tokens), False) for tokens in unlabeled_tokenized_documents_test]

    ref = []
    test = []
    
    for v, l in positive_vectorized_documents_test + unlabeled_vectorized_documents_test:
        test.append(classifier.prob_classify(v).prob(True))
        ref.append(l)    
    
    for threshold in [0.6, 0.7, 0.8, 0.9]:
        print('Threshold: %s' % threshold)
        thresholded = [e > threshold for e in test]
        print('Accuracy: %s' % accuracy(ref, thresholded))
        print(ConfusionMatrix(ref, thresholded))
    
if __name__ == '__main__':
    run()