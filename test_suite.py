from load_config import __CONFIG__
import os
from classifier import Classifier

if __name__ == '__main__':
    print("Testing classifier ...")

    classifier = Classifier(__CONFIG__, validity_checks=False)

    negative = positive = None

    with open(os.path.join(__CONFIG__['input-folder'], 'testsuite', 'negative.txt'), 'r') as file:
        negative = file.read()

    with open(os.path.join(__CONFIG__['input-folder'], 'testsuite', 'positive.txt'), 'r') as file:
        positive = file.read()

    with open(os.path.join(__CONFIG__['input-folder'], 'testsuite', 'wiki_negative.txt'), 'r') as file:
        wiki_negative = file.read()

    with open(os.path.join(__CONFIG__['input-folder'], 'testsuite', 'wiki_positive.txt'), 'r') as file:
        wiki_positive = file.read()

    with open(os.path.join(__CONFIG__['input-folder'], 'testsuite', 'input_negative.txt'), 'r') as file:
        input_negative = file.read()

    with open(os.path.join(__CONFIG__['input-folder'], 'testsuite', 'input_positive.txt'), 'r') as file:
        input_positive = file.read()        
        
    empty = ''
    space = ' '

    posp = classifier.classify(positive)
    negp = classifier.classify(negative)
    empp = classifier.classify(empty)
    spap = classifier.classify(space)
    
    wposp = classifier.classify(positive)
    wnegp = classifier.classify(negative)

    iposp = classifier.classify(input_positive)
    inegp = classifier.classify(input_negative)
    
    print("Positive document is classified as: %s [%s]" % (posp, posp > __CONFIG__['threshold']))
    print("Negative document is classified as: %s [%s]" % (negp, negp > __CONFIG__['threshold']))
    print("Empty document is classified as: %s [%s]" % (empp, empp > __CONFIG__['threshold']))
    print("Document with one space is classified as: %s [%s]" % (spap, spap > __CONFIG__['threshold']))
    print("Wiki positive document is classified as: %s [%s]" % (wposp, wposp > __CONFIG__['threshold']))
    print("Wiki negative document is classified as: %s [%s]" % (wnegp, wnegp > __CONFIG__['threshold']))
    print("Input positive document is classified as: %s [%s]" % (iposp, iposp > __CONFIG__['threshold']))
    print("Input negative document is classified as: %s [%s]" % (inegp, inegp > __CONFIG__['threshold']))

