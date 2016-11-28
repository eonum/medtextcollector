from load_config import __CONFIG__
from tokenizer import SimpleGermanTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from pprint import pprint

if __name__ == '__main__':
    print("Loading data ...")
    documents = ["This is a test document.", "This also is a document meant for testing purposes.", "And another one of those."] 
    
    print("Tokenizing ...")
    tokenizer = SimpleGermanTokenizer()
    tokenized_documents = []
    for document in documents:
        tokenized_documents.append(" ".join(tokenizer.tokenize(document)))
    
    print("Vectorizing ...")
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 
    vectorized_documents = vectorizer.fit_transform(tokenized_documents)
    
    if __CONFIG__['debug']:
        vocab = vectorizer.get_feature_names()
        print("Vocabulary: ")
        pprint(vocab)