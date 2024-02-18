import nltk
from nltk.stem.snowball import SnowballStemmer
from spellchecker import SpellChecker
import numpy as np
import string
import unidecode
from nltk.corpus import stopwords

stemmer = SnowballStemmer("french")

spell = SpellChecker(language='fr')

french_stopwords = set(stopwords.words('french'))


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))



def correct(text_toknized):
    corrected = [spell.correction(word) for word in text_toknized]
    return corrected



def tokenize(text):
    return nltk.word_tokenize(text)


def stem(word):
    return stemmer.stem(word.lower())

def remove_accents(text):
    return unidecode.unidecode(text)

def remove_stopwords(text_tokenized):
    return [word for word in text_tokenized if word not in french_stopwords]

def bag_of_words(tokenized_words, all_words):
    tokenized_words = [stem(w) for w in tokenized_words]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for s in tokenized_words:
        for i, w in enumerate(all_words):
            if w == s:
                bag[i] = 1.0
    return bag


sentence = "bonjour cà và tres boien"
sentence = tokenize(sentence)
sentence = correct(sentence)
sentence = [remove_accents(word) for word in sentence]
print(sentence)