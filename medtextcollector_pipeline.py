import os
import pickle
import random
import time
from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from vectorizer import bag_of_words
from nltk import NaiveBayesClassifier
from nltk.metrics import accuracy, ConfusionMatrix
from classifier import valid_document
import tqdm

def load_documents(path, dataset_size):
    documents = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames: 
            with open(os.path.join(dirpath, filename), 'r') as file:
                documents.append(file.read())
        break
    documents = documents[:dataset_size]
    random.shuffle(documents)
    testset_len = int(len(documents) * __CONFIG__['testset-ratio'])
       
    return documents[testset_len:], documents[:testset_len]

def unskew(dataset_a, dataset_b): 
    min_len = min(len(dataset_a), len(dataset_b))
    return dataset_a[:min_len], dataset_b[:min_len]

def clean(documents):
    return [doc for doc in documents if valid_document(doc)]

def run():
    print('Preparing base folder ... ')
    if not os.path.exists(os.path.join(__CONFIG__['base-folder'], 'classificator')):
        os.makedirs(os.path.join(__CONFIG__['base-folder'], 'classificator'))
        
    print('Loading data ...')
    max_dataset_size = __CONFIG__['max-dataset-size'] if __CONFIG__['max-dataset-size'] > 0 else None
    positive_documents_train, positive_documents_test = load_documents(os.path.join(__CONFIG__['input-folder'], 'positive'), max_dataset_size)
    unlabeled_documents_train, unlabeled_documents_test = load_documents(os.path.join(__CONFIG__['input-folder'], 'unlabeled'), max_dataset_size) 
    # unlabeled means "negative" 
        
    positive_documents_train, unlabeled_documents_train = unskew(positive_documents_train, unlabeled_documents_train)
    positive_documents_test, unlabeled_documents_test = unskew(positive_documents_test, unlabeled_documents_test)

    print("Training")
    print('Tokenizing training set ...')
    tokenizer = SimpleGermanTokenizer()
    positive_tokenized_documents_train = []
    unlabeled_tokenized_documents_train = []
    for document in tqdm.tqdm(positive_documents_train):
        positive_tokenized_documents_train.append(tokenizer.tokenize(document))
    for document in tqdm.tqdm(unlabeled_documents_train):
        unlabeled_tokenized_documents_train.append(tokenizer.tokenize(document))
    
    positive_tokenized_documents_train = clean(positive_tokenized_documents_train)
    unlabeled_tokenized_documents_train = clean(unlabeled_tokenized_documents_train)
    positive_tokenized_documents_train, unlabeled_tokenized_documents_train = unskew(positive_tokenized_documents_train, unlabeled_tokenized_documents_train)
    print('Trainingset size: ' + str(len(positive_tokenized_documents_train) + len(unlabeled_tokenized_documents_train)))
    
    print('Vectorizing training set ...')
    positive_vectorized_documents_train = [(bag_of_words(tokens), True) for tokens in tqdm.tqdm(positive_tokenized_documents_train)]
    unlabeled_vectorized_documents_train = [(bag_of_words(tokens), False) for tokens in tqdm.tqdm(unlabeled_tokenized_documents_train)]
    
    classifier =  NaiveBayesClassifier.train(positive_vectorized_documents_train + unlabeled_vectorized_documents_train)
    model_path = os.path.join(__CONFIG__['base-folder'], 'classificator','naive_bayes_model-%s.pickle' % time.strftime('%d-%m-%y-%H'))
    print("Saving model to %s ..." % model_path)    
    with open(model_path, 'wb') as file:
        pickle.dump(classifier, file)
      
    print("Evaluation")  
    print('Tokenizing test set...')
    positive_tokenized_documents_test = []
    unlabeled_tokenized_documents_test = []
    for document in tqdm.tqdm(positive_documents_test):
        positive_tokenized_documents_test.append(tokenizer.tokenize(document))
    for document in tqdm.tqdm(unlabeled_documents_test):
        unlabeled_tokenized_documents_test.append(tokenizer.tokenize(document))
    
    positive_tokenized_documents_test = clean(positive_tokenized_documents_test)
    unlabeled_tokenized_documents_test = clean(unlabeled_tokenized_documents_test)
    positive_tokenized_documents_test, unlabeled_tokenized_documents_test = unskew(positive_tokenized_documents_test, unlabeled_tokenized_documents_test)
    print('Testset size: ' + str(len(positive_tokenized_documents_test) + len(unlabeled_tokenized_documents_test)))


    print('Vectorizing test set ...')
    positive_vectorized_documents_test = [(bag_of_words(tokens), True) for tokens in tqdm.tqdm(positive_tokenized_documents_test)]
    unlabeled_vectorized_documents_test = [(bag_of_words(tokens), False) for tokens in tqdm.tqdm(unlabeled_tokenized_documents_test)]

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