# Here I am using gensim for learning the word embeddings from the EUADR corpus
# This is just a rough start to learn
import gensim
import logging
import os
import pandas as pd
import re
# start the log
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)


# download NLTK basic stopwords
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


def clean_my_text(full_text):
    # stopset = set(stopwords.words('english'))  # | set(string.punctuation)
    tokens = nltk.word_tokenize(full_text)
    cleanup = [token for token in tokens if len(token) > 2]
    return cleanup


# get the current working directory and file
data_dir_path = '/home/stirunag/Dataset/'


# tokenize.sent_tokenize(doc.lower())
class SentenceClass(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            print(fname)
            for line in open(os.path.join(self.dirname, fname), 'r', encoding='ISO-8859-1'):
                yield clean_my_text(line)




# iterate one line at a time and learn embeddings
sentences = SentenceClass(data_dir_path)  # a memory-friendly iterator
# model = gensim.models.Word2Vec(sentences)

model = gensim.models.Word2Vec(
    sentences,
    size=200,
    window=20,
    min_count=3,
    workers=8, iter=10)

logging.info("Done training data files")


model.wv.save_word2vec_format('/home/stirunag/models/model_OTAR_200d-3mc-10it.bin', binary=True)