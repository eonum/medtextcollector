def simple_bag_of_words(words):
    return dict([(word, True) for word in words])

def bag_of_words(words):
    features = {}
    for word in words:
        if word in features:
            features[word] += 1
        else:
            features[word] = 1
    return features