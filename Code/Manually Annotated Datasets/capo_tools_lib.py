#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Code to split manual annotation into train, devel and valid
# Code to convert the splits into IOB format

# (c) EMBL-EBI, September 2019
#
# Started: 23 October  2019
# Updated: 24 October  2019

_author_ = 'Santosh Tirunagari'

import os
import pandas as pd
import glob
import json
import csv
import sys

import multiprocessing

import numpy as np
import re

from nltk.tokenize import wordpunct_tokenize
from ast import literal_eval

import math
import random

import math
import random


def extract_pmc_ids_from_jsons_to_file(json_path,resulth_path, file_name):
    all_files = glob.glob(json_path + '*.json*')

    with open(os.path.join(resulth_path,file_name), 'w') as f1:
        writer = csv.writer(f1, delimiter='\t', lineterminator='\n', )
        for files in all_files:
            with open(files) as json_file_ner_rel:
                json_data = json.loads(json_file_ner_rel.read())
                for articles in json_data:
                    pmc_id = articles  # json_data[articles]
                    writer.writerow([pmc_id])


def extract_pmc_ids_from_jsons(json_path):
    all_files = glob.glob(json_path + '*.json*')
    pmc_ids = []
    for files in all_files:
        with open(files) as json_file_ner_rel:
            json_data = json.loads(json_file_ner_rel.read())
            for articles_id in json_data:
                pmc_ids.append(articles_id)

    return pmc_ids


def create_train_dev_test_splits(json_path, percentage = 0.70):

    percentage = 0.70
    iter = 0

    trainPMCids = []
    devPMCids = []
    testPMCids = []

    allPMCids = extract_pmc_ids_from_jsons(json_path)

    nLines = sum(1 for line in allPMCids)
    nTrain = int(nLines * percentage)
    nValid = math.floor((nLines - nTrain) / 2)
    nTest = nLines - (nTrain + nValid)

    deck = list(range(0, nLines))
    random.seed(2222)  # Please dont change the seed for the reproducibility
    random.shuffle(deck)

    train_ids = deck[0:nTrain]
    devel_ids = deck[nTrain:nTrain + nValid]
    test_ids = deck[nTrain + nValid:nTrain + nValid + nTest]

    for each_pmc_id in allPMCids:
        if iter in train_ids:
            trainPMCids.append(each_pmc_id.strip())
        elif iter in devel_ids:
            devPMCids.append(each_pmc_id.strip())
        else:
            testPMCids.append(each_pmc_id.strip())

        iter = iter + 1

    return trainPMCids, devPMCids, testPMCids


def find_sub_list(sl, l):
    results = []
    sll = len(sl)
    for ind in (i for i, e in enumerate(l) if e == sl[0]):
        if l[ind:ind + sll] == sl:
            results.append((ind, ind + sll))

    return results


def convert2IOB_dict(text_data, ner_tags):
    tokens = []
    ners = []

    split_text = wordpunct_tokenize(text_data)
    # for each word token append 'O'
    arr = ['O'] * len(split_text)

    if ner_tags:
        for each_tag in ner_tags:
            token_list = wordpunct_tokenize(each_tag[2])
            ner_list = wordpunct_tokenize(each_tag[3])

            if (len(token_list) > len(ner_list)):
                ner_list = len(token_list) * ner_list

            for i in range(0, len(ner_list)):
                # The logic here is look for the first B-tag and then append I-tag next
                if (i == 0):
                    ner_list[i] = 'B-' + ner_list[i]
                else:
                    ner_list[i] = 'I-' + ner_list[i]

            tokens.append(token_list)
            ners.append(ner_list)

        for i in range(0, len(tokens)):
            spans = find_sub_list(tokens[i], split_text)
            for each_span in spans:
                arr[each_span[0]:each_span[1]] = ners[i]

    return zip(split_text, arr)


from ast import literal_eval


def find_sub_list(sl, l):
    results = []
    sll = len(sl)
    for ind in (i for i, e in enumerate(l) if e == sl[0]):
        if l[ind:ind + sll] == sl:
            results.append((ind, ind + sll))

    return results


def convert2IOB_dict_manual_annotations(text_data, ner_tags):
    tokens = []
    ners = []

    split_text = wordpunct_tokenize(text_data)
    # for each word token append 'O'
    arr = ['O'] * len(split_text)

    if ner_tags != 'No-Ner':
        ner_tags = literal_eval(ner_tags)
        for each_tag in ner_tags:
            token_list = wordpunct_tokenize(each_tag[2])
            ner_list = wordpunct_tokenize(each_tag[3])

            if (len(token_list) > len(ner_list)):
                ner_list = len(token_list) * ner_list

            for i in range(0, len(ner_list)):
                # The logic here is look for the first B-tag and then append I-tag next
                if (i == 0):
                    ner_list[i] = 'B-' + ner_list[i]
                else:
                    ner_list[i] = 'I-' + ner_list[i]

            tokens.append(token_list)
            ners.append(ner_list)

        for i in range(0, len(tokens)):
            spans = find_sub_list(tokens[i], split_text)
            for each_span in spans:
                arr[each_span[0]:each_span[1]] = ners[i]

        return zip(split_text, arr)

    else:
        return zip(split_text, arr)


def convert2IOB_dict_EPMC_annotations(text_data, ner_tags):
    tokens = []
    ners = []

    split_text = wordpunct_tokenize(text_data)
    # for each word token append 'O'
    arr = ['O'] * len(split_text)

    if ner_tags != 'No-Ner':
        for each_tag in ner_tags:
            token_list = wordpunct_tokenize(each_tag[0])
            ner_list = wordpunct_tokenize(each_tag[1])

            if (len(token_list) > len(ner_list)):
                ner_list = len(token_list) * ner_list

            for i in range(0, len(ner_list)):
                # The logic here is look for the first B-tag and then append I-tag next
                if (i == 0):
                    ner_list[i] = 'B-' + ner_list[i]
                else:
                    ner_list[i] = 'I-' + ner_list[i]

            tokens.append(token_list)
            ners.append(ner_list)

        for i in range(0, len(tokens)):
            spans = find_sub_list(tokens[i], split_text)
            for each_span in spans:
                arr[each_span[0]:each_span[1]] = ners[i]

        return zip(split_text, arr)
    else:
        return zip(split_text, arr)



def create_train_dev_test_IOB_to_file(json_path, result_path, percentage_split = 0.70):

    all_files = glob.glob(json_path + '*.json*')
    trainPMCids, devPMCids, testPMCids =  create_train_dev_test_splits(json_path, percentage_split)

    with open(result_path + 'train.csv', 'w', newline='\n') as f1, open(result_path + 'dev.csv', 'w',
                        newline='\n') as f2, open(result_path + 'test.csv', 'w', newline='\n') as f3:

        train_writer = csv.writer(f1, delimiter='\t', lineterminator='\n')
        dev_writer = csv.writer(f2, delimiter='\t', lineterminator='\n')
        test_writer = csv.writer(f3, delimiter='\t', lineterminator='\n')

        for each_manually_annotated_json in all_files:
            with open(each_manually_annotated_json) as json_file_ner_rel:
                json_data = json.loads(json_file_ner_rel.read())

                for articles in json_data:
                    pmc_id = articles  # json_data[articles]
                    for each_annotation in json_data[articles]['annotations']:
                        # if each_annotation['ner'] != None:
                        text = each_annotation['sent'].encode('utf-8').decode('utf-8')
                        ner = each_annotation['ner']
                        tagged_tokens = convert2IOB_dict(text, ner)

                        if pmc_id in trainPMCids:
                            for each_word in tagged_tokens:
                                train_writer.writerow(list(each_word))
                            train_writer.writerow('')

                        elif pmc_id in devPMCids:
                            for each_word in tagged_tokens:
                                dev_writer.writerow(list(each_word))
                            dev_writer.writerow('')

                        elif pmc_id in testPMCids:
                            for each_word in tagged_tokens:
                                test_writer.writerow(list(each_word))
                            test_writer.writerow('')


def create_IOB_to_file(json_path, result_path):
    all_files = sorted(glob.glob(json_path + '*.json*'))

    with open(result_path + 'data_IOB.csv', 'w', newline='\n') as f1:
        writer = csv.writer(f1, delimiter='\t', lineterminator='\n')
        for each_manually_annotated_json in all_files:
            print(each_manually_annotated_json)
            with open(each_manually_annotated_json) as json_file_ner_rel:
                json_data = json.loads(json_file_ner_rel.read())

                for articles in json_data:
                    pmc_id = articles  # json_data[articles]
                    for each_annotation in json_data[articles]['annotations']:
                        text = each_annotation['sent'].encode('utf-8').decode('utf-8')
                        ner = each_annotation['ner']
                        tagged_tokens = convert2IOB_dict(text, ner)
                        for each_word in tagged_tokens:
                            writer.writerow(list(each_word))
                        writer.writerow('')


def pcse_ML_tagger_to_IOB(all_files, result_path, PMC_ids):
    with open(result_path + 'test_manual_annotated_on_ml.csv', 'a', newline='\n') as f1:
        public_writer = csv.writer(f1, delimiter='\t', lineterminator='\n')

        for each_manually_annotated_json in all_files:
            with open(each_manually_annotated_json) as json_file_ner_rel:
                json_data = json.loads(json_file_ner_rel.read())

                for articles in json_data:
                    pmc_id = articles  # json_data[articles]

                    if pmc_id in PMC_ids:
                        for each_annotation in json_data[articles]['annotations']:
                            # if each_annotation['ner'] != None:
                            text = each_annotation['sent'].encode('utf-8').decode('utf-8')
                            ner = each_annotation['ner']
                            tagged_tokens = convert2IOB_dict(text, ner)

                            for each_word in tagged_tokens:
                                public_writer.writerow(list(each_word))
                            public_writer.writerow('')





if __name__ == '__main__':
    # pool = multiprocessing.Pool(processes=8)
    # pool.map(process_each_split_to_extract_sentences, all_files)
    # pool.close()
    # pool.join()
    print('Generating train, dev and test sets!! Please be patient')
    # json_path = '/mnt/droplet/nfs/gns/literature/machine-learning/cleaned_dataset/'
    # ner_result_path = '/mnt/droplet/nfs/gns/literature/machine-learning/NER_Datasets/EBI_standard-IOB/'

    json_path = '/nfs/gns/literature/machine-learning/cleaned_dataset/'
    ner_result_path = '/nfs/gns/literature/machine-learning/Santosh/test_ml_ner/'

    percentage_split = 0.70

    all_files = glob.glob(json_path + '*.json*')
    trainPMCids, devPMCids, testPMCids =  create_train_dev_test_splits(json_path, percentage_split)

    # create_train_dev_test_IOB_to_file(json_path, ner_result_path, percentage_split)
    create_IOB_to_file(json_path, ner_result_path)
    print('All done!! please find the files at :' +ner_result_path)
