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

result_path = '/nfs/gns/literature/Santosh_Tirunagari/OTAR_Results/pure_ML_annotations/FullTextJan2020/'
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




def process_each_file_in_job(each_file_path):
    ss = getfileblocks(each_file_path)
    for each_article in ss:
        soup = BeautifulSoup(each_article, 'lxml')

        with open(result_path+'edited_'+each_file_path.split('/')[-1], 'at') as f:
            f.write(new_file_content)



parser = argparse.ArgumentParser(description='This script will process patch files to remove GP FPs in job folders on OTAR FullTextLoadings')
parser.add_argument("-f", "--file", nargs=1, required=True, help="OTAR ML FP Removal", metavar="PATH")
args = parser.parse_args()

process_each_file_in_job(args.file[0])


