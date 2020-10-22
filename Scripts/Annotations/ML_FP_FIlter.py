import glob
import gzip
from bs4 import BeautifulSoup
import lxml
from collections import defaultdict
from tqdm import tqdm
import requests
import random
import sys
import pathlib



import argparse

# import multiprocessing
from fuzzywuzzy import fuzz

url = 'http://ai-capo-api-lb/spaCy_ner_predictor?text_sentence='  # Load Balancer
result_path = '/nfs/gns/literature/machine-learning/Capo_full_test_ML_filtering/'

def getfileblocks(file_path):
    subFileBlocks = []

    with gzip.open(file_path, 'rt') as fh:
        for line in fh:
            if line.startswith('<!DOCTYPE article'):
                subFileBlocks.append(line)
            else:
                subFileBlocks[-1] += line

    return subFileBlocks


def GP_soup(file_soup):
    dict_sentences = defaultdict(list)
    for each_ztag in file_soup.find_all('z:uniprot'):
        try:
            gene_sentence = each_ztag.findParents('plain')[0].text
            dict_sentences[gene_sentence].append(each_ztag)
        except:
            pass
    return dict_sentences


def compare_with_ml_annotations(r, z_tags):
    agreed_z_tags = []
    for each_z_tag in z_tags:
        for each_ml_annotation in r.json()['annotations']:
            score = fuzz.token_set_ratio(each_ml_annotation[3], each_z_tag.text)
            if score == 100 and each_ml_annotation[2] == 'GP':
                agreed_z_tags.append(each_z_tag)

    return list(set(z_tags) - set(agreed_z_tags))


def get_unique_fp_tags(GP_dict_sentences):


    FP_dict_sentences = defaultdict(list)
    set_FPs = set()

    for each_uniprot_sentence, z_tags in GP_dict_sentences.items():
        # print(url + each_uniprot_sentence)
        r = requests.get(url + each_uniprot_sentence)
        if r.status_code == 200 and r.json()['status'] == 200:
            FPs = compare_with_ml_annotations(r, z_tags)
            if FPs:
                FP_dict_sentences[each_uniprot_sentence].append(FPs)
        else:
            print(each_uniprot_sentence)

    for FP_sent, FP_tag in FP_dict_sentences.items():
        for each_ztag in FP_tag[0]:
            set_FPs.add(each_ztag)

    return list(set_FPs)


def process_each_file_in_job(each_file_path):

    file_route = each_file_path.split('/')
    edited_file_name = '/'.join(file_route[8:10])
    result_file_path = result_path+edited_file_name

    pathlib.Path(result_file_path).mkdir(parents=True, exist_ok=True)

    ss = getfileblocks(each_file_path)
    for each_article in tqdm(ss):
        soup = BeautifulSoup(each_article, 'xml')
        GP_dict_sentences = GP_soup(soup)
        if GP_dict_sentences:
            unique_fps = get_unique_fp_tags(GP_dict_sentences)

            for each_fp in unique_fps:
                for tag in soup.findAll('z:uniprot', attrs={'ids':each_fp['ids']}):
                    tag.unwrap()

            new_file_content = str(soup).replace('<?xml version="1.0" encoding="utf-8"?>\n','').replace('</ebiroot>','</ebiroot>\n')

            with gzip.open(result_file_path+'/'+'capo_'+file_route[-1], 'at') as f:
                f.write(new_file_content)



parser = argparse.ArgumentParser(description='This script will process patch files to remove GP FPs in job folders on FullTextLoadings')
parser.add_argument("-f", "--file", nargs=1, required=True, help="ML FP Removal", metavar="PATH")
args = parser.parse_args()

process_each_file_in_job(args.file[0])


