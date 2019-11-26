from flair.data import Corpus
from flair.datasets import ColumnCorpus

columns = {0: 'text', 1: 'ner'}

# this is the folder in which train, test and dev files reside
data_folder = '/nfs/gns/literature/machine-learning/Datasets/NER_Datasets/EBI_standard-IOB'

# init a corpus using column format, data folder and the names of the train, dev and test files
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.csv',
                              test_file='test.csv',
                              dev_file='dev.csv')
tag_type = 'ner'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary.idx2item)


from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, PooledFlairEmbeddings, ELMoEmbeddings
from typing import List
embedding_types: List[TokenEmbeddings] = [
    PooledFlairEmbeddings('pubmed-forward'),
    PooledFlairEmbeddings('pubmed-backward')
]
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)
#  initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

#  start training
trainer.train('/nfs/gns/literature/Santosh_Tirunagari/GitHub/flair_models/ner/multi_bio_ner_model/EBI/300/v1/',
              learning_rate=0.1,
              mini_batch_size=16,
              patience=3,
              max_epochs=150)
