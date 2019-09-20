#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Code to split manual annotation into train, devel and valid
# Code to convert the splits into IOB format

# (c) EMBL-EBI, September 2019
#
# Started: 19 Septmember  2019
# Updated: 20 Septmember  2019

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

import math
import random


colNames = ('text', 'ner')

file_path = '/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/'
all_files = glob.glob(file_path+'*fulltext_batch*')
result_folder = '/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/NER/'


# get all the pmc ids

with open('/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/NER/list_pmc_ids.csv','w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    
    for files in all_files:
        with open(files) as json_file_ner_rel:
            json_data = json.loads(json_file_ner_rel.read())
            for articles in json_data:
                pmc_id = articles #json_data[articles]
                writer.writerow([pmc_id])
                


# Generate train, test and dev pmc ids

file = '/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/NER/list_pmc_ids.csv'
percentage=0.70
iter = 0

trainPMCids = []
devPMCids = []
testPMCids =[]

with open(file, 'r',encoding="utf-8") as fin:
    allPMCids = fin.readlines()
    
nLines = sum(1 for line in allPMCids)
nTrain = int(nLines*percentage) 
nValid = math.floor((nLines - nTrain)/2)
nTest = nLines - (nTrain+nValid)

deck = list(range(0, nLines))
random.seed(2222) # Please dont change the seed for the reproducibility 
random.shuffle(deck)

train_ids = deck[0:nTrain]
devel_ids = deck[nTrain:nTrain+nValid]
test_ids = deck[nTrain+nValid:nTrain+nValid+nTest]

for each_pmc_id in allPMCids:
    if iter in train_ids:
        trainPMCids.append(each_pmc_id.strip())
    elif iter in devel_ids:
        devPMCids.append(each_pmc_id.strip())
    else:
        testPMCids.append(each_pmc_id.strip())

    iter = iter+1       
    

# convert a sentence into a IOB format

def convert2IOB_dict(text_data,ner_tags):
    
    split_text = wordpunct_tokenize(text)
    # for each word token append 'O'
    arr = ['O']*len(split_text)
    IOB_dict = dict(zip(split_text,arr))

    ner_dict_ = {}

    for each_tag in ner:
        token_list = wordpunct_tokenize(each_tag[2])
        ner_list = wordpunct_tokenize(each_tag[3])

        if(len(token_list) > len(ner_list)):
            ner_list = len(token_list) * ner_list

        for i in range(0,len(ner_list)):
            if(i==0):
                ner_list[i] = 'B-'+ner_list[i]
            else:
                ner_list[i] = 'I-'+ner_list[i]


        ner_dict_.update(dict(zip(token_list,ner_list)))


    IOB_dict.update(ner_dict_)
    
    return IOB_dict, split_text
    

# Change the result path to yours
result_path = '/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/NER/'

with open(result_path+'train.csv','w') as f1, open(result_path+'dev.csv','w') as f2, open(result_path+'test.csv','w') as f3:  
    train_writer=csv.writer(f1, delimiter='\t',lineterminator='\n')
    dev_writer=csv.writer(f2, delimiter='\t',lineterminator='\n')
    test_writer=csv.writer(f3, delimiter='\t',lineterminator='\n')
    
    for each_manually_annotated_json in all_files:
        with open(each_manually_annotated_json) as json_file_ner_rel:
            json_data = json.loads(json_file_ner_rel.read())

            for articles in json_data:
                pmc_id = articles #json_data[articles]
                for each_annotation in json_data[articles]['annotations']:
                    if each_annotation['ner'] != None:
                        text = each_annotation['sent'].encode('utf-8').decode('utf-8')
                        ner = each_annotation['ner']
                        IOB_converted_dict, word_tokens = convert2IOB_dict(text,ner)
                        
                        if pmc_id in trainPMCids:
                            for each_word in word_tokens:
                                row = [each_word,IOB_converted_dict[each_word]]
                                train_writer.writerow(row)
                            train_writer.writerow('\n')

                        elif pmc_id in devPMCids:
                            for each_word in word_tokens:
                                row = [each_word,IOB_converted_dict[each_word]]
                                dev_writer.writerow(row)
                            dev_writer.writerow('\n')

                        elif pmc_id in testPMCids:
                            for each_word in word_tokens:
                                row = [each_word,IOB_converted_dict[each_word]]
                                test_writer.writerow(row)
                            test_writer.writerow('\n')


# if __name__ == '__main__':
    # pool = multiprocessing.Pool(processes=8)
    # pool.map(process_each_split_to_extract_sentences, all_files)
    # pool.close()
    # pool.join()
    # print('done')
