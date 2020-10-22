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
import io

import argparse

result_path = '/nfs/production/literature/Santosh_Tirunagari/GP_DS_jsonl_Extracted/ABS/'
pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)


def get_GP_tags(file_soup):
    gene_tags =[]
    for each_ztag in file_soup.find_all('uniprot'):
        gene_tags.append(each_ztag.text)
    return list(set(gene_tags))


def get_DS_tags(file_soup):
    disease_tags = []
    for each_ztag in file_soup.find_all('efo'):
        disease_tags.append(each_ztag.text)
    return list(set(disease_tags))


def process_each_file_in_job(each_file_path):
    
    with io.open(each_file_path, 'r', encoding='utf8') as fh:
        abs_text_content = fh.read()
        
    ss = abs_text_content.split('<PubmedArticle xmlns:z="ebistuff">\n')
    subFileBlocks = ss[1:]
    
    article_tags_dict ={}
    
    for each_article in tqdm(subFileBlocks):
        soup = BeautifulSoup(each_article, 'xml')
        
        try:
            pm_id = 'PMID'+soup.find('PMID').text #"article-id"
        except:
            pm_id = 'PMID'
        
        GP_list = get_GP_tags(soup)
        DS_list = get_DS_tags(soup)
#         print(GP_list)
        article_tags_dict['pmid'] = pm_id
        article_tags_dict['GP'] = GP_list
        article_tags_dict['DS'] = DS_list

        with io.open(result_path+'tags_'+each_file_path.split('/')[-1][:-3]+'jsonl', 'a', encoding='utf8') as f:
            json.dump(article_tags_dict,f, ensure_ascii=False)#.decode('unicode-escape').encode('utf8') #,indent = 2
            f.write('\n')



parser = argparse.ArgumentParser(description='This script will process patch files to extract GP DSs in job folders on OTAR FullTextLoadings')
parser.add_argument("-f", "--file", nargs=1, required=True, help="OTAR GP DS extractor to Jsonl format", metavar="PATH")
args = parser.parse_args()

process_each_file_in_job(args.file[0])

