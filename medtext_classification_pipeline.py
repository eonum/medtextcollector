import os
import pickle
import random
import time
from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, precision_score, recall_score
from classifier import valid_document
import tqdm
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

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

    print("Training ...")
    tokenizer = SimpleGermanTokenizer()
    gt = []
    for document in positive_documents_train:
        gt.append('medical')
    for document in unlabeled_documents_train:
        gt.append('nonmedical')
    
    pipeline = Pipeline([
    ('vectorizer',  TfidfVectorizer(tokenizer=tokenizer.tokenize)),
    ('classifier',  MultinomialNB()) ])
    
    pipeline.fit(positive_documents_train + unlabeled_documents_train, gt)

    model_path = os.path.join(__CONFIG__['base-folder'], 'classificator','pipeline-%s.pickle' % time.strftime('%d-%m-%y-%H'))
    print("Saving model to %s ..." % model_path)    
    with open(model_path, 'wb') as file:
        pickle.dump(pipeline, file)

    print('Testing ...')
    gt_test = []
    for document in tqdm.tqdm(positive_documents_test):
        gt_test.append('medical')
    for document in tqdm.tqdm(unlabeled_documents_test):
        gt_test.append('nonmedical')
        
    predictions = pipeline.predict(positive_documents_test+unlabeled_documents_test)
    print(confusion_matrix(gt_test, predictions))
    print('F1: %s'  % f1_score(gt_test, predictions, pos_label='medical'))
    print('Accuracy: %s' % accuracy_score(gt_test, predictions))
    print('Precision: %s' % precision_score(gt_test, predictions, pos_label='medical'))
    print('Recall: %s' % recall_score(gt_test, predictions, pos_label='medical'))
    
    
if __name__ == '__main__':
    run()