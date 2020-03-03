# Code to evaluate EPMC annotation to the Manual Annotation
# Code to compare results from ML methods and EPMC annotation

# (c) EMBL-EBI, September 2019
#
# Started: 23 Septmember  2019
# Updated: 24 Septmember  2019

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

import requests
# from pprint import pprint
import pandas as pd

from collections import defaultdict, Counter
import time
from requests.compat import urljoin

from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report

import capo_tools_lib


def get_Json_through_PMCID(pmcid):
    base_url = "https://www.ebi.ac.uk/europepmc/annotations_api/"
    article_url = urljoin(base_url,
                          "annotationsByArticleIds?articleIds=PMC%3A" + pmcid + "&provider=Europe%20PMC&format=JSON")
    r = requests.get(article_url)

    if r.status_code == 200:
        return r
    else:
        return False


def get_epmc_annotations_to_file(result_path, PMCids):
    # result_path = '/nfs/gns/literature/Santosh_Tirunagari/EPMC Annotations Dataset/'

    with open(result_path + 'EPMC_annotations.csv', 'w', newline='\n') as f1:
        test_writer = csv.writer(f1, delimiter='\t', lineterminator='\n')

        count = 0
        for each_test_pmc_id in PMCids:
            count = count+1
            print(each_test_pmc_id + '\t' + str(count))
            ss = get_Json_through_PMCID(each_test_pmc_id[3:])  # Just the number is needed. So remove the PMC from the front
            if ss:
                json_results = ss.json()
                try:
                    pmc_id = json_results[0]['pmcid']
                    # print(pmc_id)
                    for each_annotation in json_results[0]['annotations']:
                        exact = each_annotation['prefix'] + each_annotation['exact'] + each_annotation['postfix']
                        token = each_annotation['tags'][0]['name']
                        ner = each_annotation['type']
                        row = [pmc_id, exact, token, ner]
                        test_writer.writerow(row)
                except(IndexError):
                    print('no annotations found!!')
            else:
                continue


def extract_sentences_from_sentencised_xml(result_path, path_to_PMCids):
    all_files = sorted(glob.glob(path_to_PMCids + '*.xml'))

    with open(result_path + 'full_sentences.csv', 'w', newline='\n') as f1:
        test_writer = csv.writer(f1, delimiter='\t', lineterminator='\n')

        count = 0
        for each_test_pmc_id in all_files:
            count = count+1
            pmc_id = os.path.basename(each_test_pmc_id)[:-4]
            print(pmc_id + '\t' + str(count))

            with open(each_test_pmc_id, 'r') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                for each_sent in soup.find_all('plain'):
                    row = [pmc_id, each_sent.text]
                    test_writer.writerow(row)



def convert_partial_sentences_to_full(path_to_csv_annotationAPI_sentences, path_to_csv_full_sentences,path_to_xml, result_path):

    annotation_sent_csv = pd.read_csv(path_to_csv_annotationAPI_sentences, names=['pmc_id', 'sentence', 'token', 'ner'], sep='\t')
    full_sent_csv =  pd.read_csv(path_to_csv_full_sentences, names=['pmc_id', 'sentence'],
                                 sep='\t')

    # xml_path = '/nfs/gns/literature/machine-learning/benchmarking/benchmark_sent/'
    all_files = sorted(glob.glob(path_to_xml + '*.xml'))
    names = [os.path.basename(x) for x in all_files]
    PMC_ids = [x[:-4] for x in names]

    count = 0


    for each_pmc_id in PMC_ids:
        count = count + 1
        print(each_pmc_id + '\t' + str(count))

        pmc_id_annotation_sents = annotation_sent_csv[annotation_sent_csv['pmc_id'] == each_pmc_id]
        pmc_id_full_sentences = full_sent_csv[full_sent_csv['pmc_id'] == each_pmc_id]
        pmc_id_full_sentences_list = pmc_id_full_sentences['sentence'].tolist()

        full_sentences_match = []
        for iter_a, rows_a in pmc_id_annotation_sents.iterrows():
            try:
                res = [x for x in pmc_id_full_sentences_list if re.search(re.escape(rows_a['sentence']), x)]
                full_sentences_match.append(res[0])
            except:
                full_sentences_match.append('None')

        if full_sentences_match:
            pmc_id_annotation_sents = pmc_id_annotation_sents.assign(full_sentence=full_sentences_match)
            pmc_id_annotation_sents['combined'] = pmc_id_annotation_sents.apply(lambda x: list([x['token'], x['ner']]),
                                                                                        axis=1)
            sent_tags = pmc_id_annotation_sents.groupby('full_sentence')['combined'].apply(list).reset_index(name='tags')
            pmc_id_full_sentences.rename(columns={'sentence': 'full_sentence'}, inplace=True)
            epmc_full_sentence_tags = pd.merge(pmc_id_full_sentences, sent_tags, on='full_sentence', how='left')

            epmc_full_sentence_tags.to_csv(result_path+'Europe_PMC_annotation.csv', mode='a', header=False, sep='\t', index=False)
        else:
            pmc_id_full_sentences.to_csv(result_path+'Europe_PMC_annotation.csv', mode='a', header=False, sep='\t', index=False)


def sentences_tags(pmc_id, result_path, path_manual_annot_csv):
    manual_annot_csv = pd.read_csv(path_manual_annot_csv, names=['pmc_id', 'sent_id', 'sentence', 'ner', 'relation'], sep='\t')
    manual_annot_csv = manual_annot_csv[manual_annot_csv['ner'] != 'No-Ner']

    EPMC_annot_csv = pd.read_csv(result_path + 'EPMC_annotations_.csv', names=['pmc_id', 'sentence', 'token', 'ner'],
                                 sep='\t')


    all_europe_pm_sentences = EPMC_annot_csv[EPMC_annot_csv['pmc_id'] == pmc_id]['sentence'].tolist()
    manual_annotated_sentences = manual_annot_csv[manual_annot_csv['pmc_id'] == pmc_id]['sentence'].tolist()

    full_sentences = []
    for each_sentence in tqdm(all_europe_pm_sentences):
        try:
            res = [x for x in manual_annotated_sentences if re.search(re.escape(each_sentence), x)]
            full_sentences.append(res[0])
        except:
            full_sentences.append('None')

    new_epmc = EPMC_annot_csv[EPMC_annot_csv['pmc_id'] == pmc_id]
    new_epmc = new_epmc.assign(full_sentence=full_sentences)
    new_epmc['combined'] = new_epmc.apply(lambda x: list([x['token'], x['ner']]), axis=1)
    sent_tags = new_epmc.groupby('full_sentence')['combined'].apply(list).reset_index(name='tags')

    new_man_annot = manual_annot_csv[manual_annot_csv['pmc_id'] == pmc_id]
    new_man_annot = manual_annot_csv[manual_annot_csv['pmc_id'] == pmc_id].reset_index()
    new_man_annot.rename(columns={'sentence': 'full_sentence'}, inplace=True)
    epmc_sentence_tags = pd.merge(new_man_annot, sent_tags, on='full_sentence', how='left')

    return epmc_sentence_tags


def convert_epmc_manual_annotations_IOB_format_to_file(result_path):
    with open(result_path + 'EPMC_annotated_test.csv', 'w', newline='\n') as f1, open(
            result_path + 'manual_annotated_test.csv', 'w', newline='\n') as f2:
        epmc_writer = csv.writer(f1, delimiter='\t', lineterminator='\n')
        manual_writer = csv.writer(f2, delimiter='\t', lineterminator='\n')

        for each_pmc_id in testPMCids:
            print(each_pmc_id)
            ss_ = sentences_tags(each_pmc_id, EPMC_annot_csv, manual_annot_csv)
            ss = ss_.where((pd.notnull(ss_)), 'No-Ner')
            for index, row in tqdm(ss.iterrows(), total=ss.shape[0]):
                tagged_tokens = capo_tools_lib.convert2IOB_dict_EPMC_annotations(row['full_sentence'], row['tags'])
                for each_word in tagged_tokens:  # make it to manual annotation format for easy comparison
                    epmc_tokens = list(each_word)
                    if epmc_tokens[1] == 'B-Diseases':
                        epmc_tokens[1] = 'B-DS'
                    elif epmc_tokens[1] == 'I-Diseases':
                        epmc_tokens[1] = 'I-DS'
                    elif epmc_tokens[1] == 'B-Organisms':
                        epmc_tokens[1] = 'B-OG'
                    elif epmc_tokens[1] == 'I-Organisms':
                        epmc_tokens[1] = 'I-OG'
                    elif epmc_tokens[1] == 'B-Gene_Proteins':
                        epmc_tokens[1] = 'B-GP'
                    elif epmc_tokens[1] == 'I-Gene_Proteins':
                        epmc_tokens[1] = 'I-GP'
                    else:
                        epmc_tokens[1] = 'O'
                    epmc_writer.writerow(epmc_tokens)
                epmc_writer.writerow('')
                manual_tagged_tokens = capo_tools_lib.convert2IOB_dict_manual_annotations(row['full_sentence'], row['ner'])
                for each_word in manual_tagged_tokens:
                    manual_writer.writerow(list(each_word))
                manual_writer.writerow('')


def evaluate_epmc_manual_annotations(result_path, type):

    true_lbs = pd.read_csv(result_path + 'manual_annotated_test.csv', sep='\t', names=['tokens', 'tags'])
    pred_lbs = pd.read_csv(result_path + 'EPMC_annotated_test.csv', sep='\t', names=['tokens', 'tags'])

    if type =='ib-wise':
        y_true = true_lbs['tags'].values
        y_pred = pred_lbs['tags'].values
    else:
        true_lbs['tags'].replace('B-|I-', '', regex=True, inplace=True)
        pred_lbs['tags'].replace('B-|I-', '', regex=True, inplace=True)

        y_true = true_lbs['tags'].values
        y_pred = pred_lbs['tags'].values

    class_labels = sorted([tag for tag in set(y_true) if tag != 'O'], key=lambda name: (name[1:], name[0]))
    print(classification_report(y_true, y_pred, labels=class_labels))
    result_dict = classification_report(y_true, y_pred, labels=class_labels, output_dict=True)


    return result_dict

if __name__ == '__main__':

    print('Evaluating EPMC vs ML NER !! Please be patient')

    # result_path = '/nfs/gns/literature/machine-learning/EPMC_annotations/annotations_API/'
    xml_path = '/nfs/gns/literature/machine-learning/benchmarking/benchmark_sent/'
    # all_files = sorted(glob.glob(xml_path + '*.xml'))
    # names = [os.path.basename(x) for x in all_files]
    # PMC_ids = [x[:-4] for x in names]

    # type = 'non-ib'
    # get_epmc_annotations_to_file(result_path, PMC_ids)
    # result =  evaluate_epmc_manual_annotations(result_path, type)
    result_path = '/nfs/gns/literature/machine-learning/EPMC_annotations/full_sentences/'
    # extract_sentences_from_sentencised_xml(result_path, xml_path)

    path_to_csv_annotationAPI_sentences = '/nfs/gns/literature/machine-learning/EPMC_annotations/annotations_API/EPMC_annotations.csv'
    path_to_csv_full_sentences = '/nfs/gns/literature/machine-learning/EPMC_annotations/full_sentences/full_sentences.csv'
    convert_partial_sentences_to_full(path_to_csv_annotationAPI_sentences, path_to_csv_full_sentences, xml_path,
                                      result_path)



    print('All done!!')
