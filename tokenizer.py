import re
import nltk
from nltk.stem.snowball import GermanStemmer
from nltk.corpus import stopwords

def setup():
    # setup needed libraries, directories etc. TODO construct need directories automatically
    nltk.download('punkt')

class TokenizerBase():
    def split_to_words(self, s, delimiter='[.,?!:; {}()"\[" "\]"" "\n"]'):
        l = re.split(delimiter, s)
        l = [v for v in l if v != ''] #remove all empty strings
        return l

    def replace_umlauts(self, text):
        res = text
        return res

    def replace_special_chars(self, text):
        res = text
        res = res.replace(u'ß', 'ss')
        res = res.replace(u'—', '-')
        return res


class SimpleGermanTokenizer(TokenizerBase):
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

class NonStemmingTokenizer(TokenizerBase):
    # https://github.com/devmount/GermanWordEmbeddings/blob/master/preprocessing.py
    def tokenize(self, s):
        # punctuation and stopwords
        punctuation_tokens = ['.', '..', '...', ',', ';', ':', '"', u'„', '„', u'“', '“', '\'',
                              '[', ']', '{', '}', '(', ')', '<', '>', '?', '!', '-', u'–', '+',
                              '*', '--', '\\', '\'\'', '``', '‚', '‘', '\n', '\\n', '']

        punctuation = ['?', '.', '!', '/', ';', ':', '(', ')', '&', '\n']

        # Define at which chars you want to split words
        # split_chars = ['-', '/', '\\\\', '+', '|']
        split_chars = ['/', '\\\\', '+', '|']
        # stop_words = [self.replace_umlauts(token) for token in stopwords.words('german')]


        # replace umlauts
        s = self.replace_umlauts(s)

        # replace newline chars
        def remove_newlines(document):
            document = re.sub('\\n', ' ', document)
            document = re.sub('\\\\n', ' ', document)
            document = re.sub('\n', ' ', document)

            return document

        s = remove_newlines(s)

        s = self.replace_special_chars(s)

        # get word tokens
        words = nltk.word_tokenize(s)


        # filter punctuation tokens
        words = [x for x in words if x not in punctuation_tokens]

        # remove stopwords
        # words = [x for x in words if x not in stop_words]

        # split words at defined characters
        delimiters = '[' + "".join(split_chars) + ']'

        flat_words = []
        for x in words:
            flat_words.extend(re.split(delimiters, x))

        words = flat_words


        # functions to remove all punctuations at the beginning and end of a word
        # (in case something in the nltk.word_tokenize() was left over)
        def remove_start_punct(word):
            while word and (word[0] in punctuation_tokens):
                word = word[1:]
            return word

        def remove_end_puntc(word):
            while word and (word[-1] in punctuation_tokens):
                word = word[:-1]
            return word

        # remove all punctuations at the beginning and ending of a word
        words = [remove_start_punct(x) for x in words]
        words = [remove_end_puntc(x) for x in words]

        # remove all undesired punctuations at any location
        words = [re.sub('[' + "".join(punctuation) + ']', '', x) for x in words]

        # process words
        words = [x.lower() for x in words]

        # remove everything except
        words = [re.sub(r'[^a-z0-9%ÜÖÄÉÈÀéèàöäü=><†@≥≤\s\-\/]', '', x) for x in words]

        # remove stopwords TODO activate maybe
        # words = [x for x in words if x not in stop_words]

        return words 

    
def get_tokenizer(tk):
    if tk == 'sgt':
        tokenizer = SimpleGermanTokenizer()
    elif tk == 'nst':
        tokenizer = NonStemmingTokenizer()
    else:
        # Default
        print("Warning: Couldn't find specified tokenizer. Continuing with default tokenizer. ")
        tokenizer = NonStemmingTokenizer()

    return tokenizer