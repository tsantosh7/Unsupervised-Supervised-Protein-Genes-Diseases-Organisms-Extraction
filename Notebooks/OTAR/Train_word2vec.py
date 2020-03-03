# Here I am using gensim for learning the word embeddings from the OTAR
# This is just a rough start to learn
import gensim
import logging
import os


# start the log
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)



import spacy
nlp = spacy.load('en_core_sci_sm')



def clean_my_text(full_text):
    # stopset = set(stopwords.words('english')) #| set(string.punctuation)
    doc = nlp(full_text)
    tokens = [token.text for token in doc]
    cleanup = [token for token in tokens if len(token) > 1 and ~token.isdigit()]
    return cleanup


# get the current working directory and file
data_dir_path = '/home/stirunag/Work/OTAR dumps/Toy/'
result_dir_path = '/home/stirunag/pre-trained_word_embeddings/OTAR_SciSpacy/'

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


model = gensim.models.Word2Vec(
    sentences,
    size=200,
    window=20,
    min_count=2,
    sg=1,
    hs=0,
    workers=8, iter=5)

logging.info("Done training data files")


model.wv.save_word2vec_format(result_dir_path+'full_model_OTAR_200d_6_iter_20mc.bin', binary=True)


