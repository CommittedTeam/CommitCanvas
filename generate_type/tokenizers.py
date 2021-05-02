import nltk
from nltk.corpus import stopwords

def stem_tokenizer(text):
    """Do stemming on words"""
    ps = nltk.PorterStemmer()
    tokens = [word for word in nltk.word_tokenize(text) if (word.isalpha() and word not in stopwords.words('english'))] 
    stems = [ps.stem(item) for item in tokens]
    return stems

def dummy(doc):
    return doc