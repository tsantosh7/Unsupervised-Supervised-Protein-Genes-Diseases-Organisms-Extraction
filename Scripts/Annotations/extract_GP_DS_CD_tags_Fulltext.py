# This script will process patch files to remove GP FPs in job folders on OTAR FullTextLoadings
# (c) EMBL-EBI, Jan 2020
#
# Started: 15 Sept 2020
# Updated: 13 Oct  2020

_author_ = 'Santosh Tirunagari'


import logging
import torch
from torch.utils.data import DataLoader
import pickle
from biobert.model.bert_crf_model import BertCRF
from biobert.data_loader.epmc_loader import NERDatasetBatch
from biobert.utils.utils import my_collate
from nltk.tokenize import WordPunctTokenizer
from collections import namedtuple

import gzip
import glob
from bs4 import BeautifulSoup
import lxml
from collections import defaultdict
from tqdm import tqdm
import requests
import random
import sys
import pathlib
import json
import io

import argparse

# import multiprocessing
from fuzzywuzzy import fuzz

tokenizer = WordPunctTokenizer()

Entity = namedtuple('Entity', ['span', 'tag', 'text', 'pre', 'post'])
Entity_Label = namedtuple('Label', ['index', 'pos', 'tag', 'span'])


class MLModel:
    def __init__(self):
        self.bertCrf_model = load_model()

        # bertCrf_model.load_state_dict(torch.load('/homes/yangx/home/gitrepo/biobertepmc/model/bert_crf_model.states', map_location=device))
        self.bertCrf_model.load_state_dict(torch.load(MODEL_PATH+'bert_crf_model.states', map_location=device))
        self.bertCrf_model.bert_model.bert_model.to(device)

    def post(self, sentences):
        BATCH_SIZE = 16
        text = sentences
        # print(text)
        with torch.no_grad():
            processor, tokens, spans = load_data_processor(text)
            dataLoader = DataLoader(dataset=processor, batch_size=BATCH_SIZE, collate_fn=my_collate, num_workers=2)

            idx2label = params['idx2label']
            self.bertCrf_model.eval()
            entities = []
            for i_batch, sample_batched in enumerate(dataLoader):
                inputs = sample_batched['input']

                bert_inputs, bert_attention_mask, bert_token_mask, wordpiece_alignment, split_alignments, lengths, token_mask \
                    = processor.tokens_totensor(inputs)

                _, preds = self.bertCrf_model.predict(input_ids=bert_inputs.to(device),
                                                 bert_attention_mask=bert_attention_mask.to(device),
                                                 bert_token_mask=bert_token_mask,
                                                 alignment=wordpiece_alignment,
                                                 splits=(split_alignments, lengths),
                                                 token_mask=token_mask)
                if idx2label:
                    for i, (path, score) in enumerate(preds):
                        labels = [idx2label[p] for p in path]
                        offset_index = i_batch*BATCH_SIZE + i
                        entities.append([[e.span[0], e.span[1], e.tag, e.text]
                                         for e in extract_entity(labels, spans[offset_index], text[offset_index])])
        return {'annotations': entities}


def load_data_processor(inputs):
    token_spans = []
    tokens = []
    for line in inputs:
        token_spans.append(list(tokenizer.span_tokenize(line)))
        tokens.append([line[start: end] for start, end in token_spans[-1]])

    processor = NERDatasetBatch.from_params(params=params, inputs=tokens)
    return processor, tokens, token_spans


def load_model():
    allowed_transitions = None
    model = BertCRF(num_tags=params['num_tags'],
                    model_name=params['model_name'],
                    stride=params['stride'],
                    include_start_end_transitions=True,
                    constraints=allowed_transitions)
    return model


def extract_entity(preds, spans, text, length=20):
    """
    extract entity from label sequence
    :param preds: a list of labels in a sentence
    :type preds: List[str
    :param spans:
    :type spans:
    :return: A list of entity object
    :rtype: List[Entity]
    """
    entities = []
    tmp = []

    for i, token in enumerate(preds):
        if token == 'O':
            pos, tag = 'O', 'O'
            label = None
        else:
            pos, tag = token.split('-')
            label = Entity_Label(index=i, pos=pos, tag=tag, span=spans[i])

        if pos in {'B', 'O'} and tmp:
            start_span = tmp[0].span[0]
            end_span = tmp[-1].span[1]
            entities.append(Entity(span=(start_span, end_span),
                                   tag=tmp[0].tag,
                                   text=text[start_span:end_span],
                                   pre=text[max(0, start_span-length):start_span],
                                   post=text[end_span: end_span+length]))
            tmp[:] = []
        if pos == 'B' or pos == 'I':
            tmp.append(label)

    if tmp:
        start_span = tmp[0].span[0]
        end_span = tmp[-1].span[-1]
        entities.append(
            Entity(span=(start_span, end_span),
                   tag=tmp[0].tag,
                   text=text[start_span:end_span],
                   pre=text[max(0, start_span-length):start_span],
                   post=text[end_span:end_span+length])
                   )
    return entities



def getfileblocks(file_path):
    subFileBlocks = []

    with io.open(file_path, 'r', encoding='utf8') as fh:
        for line in fh:
            if line.startswith('<!DOCTYPE'):
                subFileBlocks.append(line)
            else:
                subFileBlocks[-1] += line

    return subFileBlocks


def get_GP_tags(file_soup):
    gene_tags =[]
    for each_ztag in file_soup.find_all('z:uniprot'):
        gene_tags.append(each_ztag.text)
    return list(set(gene_tags))


def get_DS_tags(file_soup):
    disease_tags = []
    for each_ztag in file_soup.find_all('z:efo'):
        disease_tags.append(each_ztag.text)
    return list(set(disease_tags))


def get_CD_tags(file_soup):
    all_sentences = []
    ChemD_tags = []
    for each_sentence in file_soup.find_all('plain'):
        all_sentences.append(each_sentence.text)
    
    #sentences_found = find_all_sentences(soup)
    ML_annotations = ml_model.post(all_sentences)

    for each_ml_annotation in ML_annotations['annotations']:
        if len(each_ml_annotation) != 0:
            print(each_ml_annotation)
            for notation in each_ml_annotation:
                ChemD_tags.append(notation[3])

    return list(set(ChemD_tags))


def process_each_file_in_job(each_file_path):
    ss = getfileblocks(each_file_path)
    article_tags_dict ={}
    
    for each_article in tqdm(ss):
        soup = BeautifulSoup(each_article, 'lxml')
        
        try:
            pm_id = 'PMC'+soup.find(attrs={"pub-id-type" : "pmcid"}).text #"article-id"
        except:
            pm_id = 'PMC'
        
        GP_list = get_GP_tags(soup)
        DS_list = get_DS_tags(soup)
        CD_list = get_CD_tags(soup)

        article_tags_dict['pmid'] = pm_id
        article_tags_dict['GP'] = GP_list
        article_tags_dict['DS'] = DS_list
        article_tags_dict['CD'] = CD_list


        with io.open(result_path+'tags_'+each_file_path.split('/')[-1][:-3]+'jsonl', 'a', encoding='utf8') as f:
            json.dump(article_tags_dict,f) #,indent = 2
            f.write('\n')


if __name__ == "__main__":
    """
    NOTE: When use on cluster, make sure you use the correct file/directory path on nfs 
    instead of path on your local machine.
    """
    # if a machine learning service is used, provide the url endpoint for predictions.
    # otherwise leave it as None and a model will be set up on cluster node
    # url = 'http://ai-capo-api-lb/predict/sent'  # Load Balancer
    # url = "http://127.0.0.1:5001/predict/sent"
    url = None
    # path to save the filtered results
    result_path = '/nfs/production/literature/Santosh_Tirunagari/GP_DS_CD_jsonl_Extracted/Fulltext/'
    pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)

    MODEL_PATH = '/nfs/misc/literature/machine-learning/Santosh/Gitlab/biobertepmc/reproduce_ChemD/1602771168/'

    # path to the file that has model parameters
    params_path = MODEL_PATH+"params.pickle"
    with open(params_path, 'rb') as f:
        params = pickle.load(f)
    params['max_ner_token_len'] = -1
    params['max_bert_token_len'] = -1

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    parser = argparse.ArgumentParser(description='This script will process OATR dump to extract GP, DS, CD tags on FullTextLoadings')
    parser.add_argument("-f", "--file", nargs=1, required=True, help="Tag extractor OTAR", metavar="PATH")
    args = parser.parse_args()

    if not url:
        ml_model = MLModel()

    process_each_file_in_job(args.file[0])
