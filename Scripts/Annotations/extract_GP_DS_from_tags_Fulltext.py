# This script will process patch files to remove GP FPs in job folders on OTAR FullTextLoadings
# (c) EMBL-EBI, Jan 2020
#
# Started: 15 Sept 2020
# Updated: 13 Oct  2020

_author_ = 'Santosh Tirunagari'

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
import json


import argparse

# import multiprocessing
from fuzzywuzzy import fuzz

result_path = '/nfs/production/literature/Santosh_Tirunagari/GP_DS_jsonl_Extracted/'

pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)

def getfileblocks(file_path):
    subFileBlocks = []

    with open(file_path, 'r') as fh:
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
        
        article_tags_dict['pmid'] = pm_id
        article_tags_dict['GP'] = GP_list
        article_tags_dict['DS'] = DS_list

        with open(result_path+'tags_'+each_file_path.split('/')[-1][:-3]+'jsonl', 'at') as f:
            json.dump(article_tags_dict,f) #,indent = 2
            f.write('\n')



parser = argparse.ArgumentParser(description='This script will process patch files to extract GP DSs in job folders on OTAR FullTextLoadings')
parser.add_argument("-f", "--file", nargs=1, required=True, help="OTAR GP DS extractor to Jsonl format", metavar="PATH")
args = parser.parse_args()

process_each_file_in_job(args.file[0])

