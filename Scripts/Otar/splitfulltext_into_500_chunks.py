#!/usr/bin/env python
# coding: utf-8

# This script will process patch files to remove GP FPs in job folders on OTAR FullTextLoadings
# (c) EMBL-EBI, Jan 2020
#
# Started: 15 Sept 2020
# Updated: 13 Oct  2020


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
import csv
import pandas as pd

import argparse

result_path = '/nfs/production/literature/Santosh_Tirunagari/20.11_FT_Chunks/'
chunck_size = 100

# all_article_files = glob.glob('/nfs/production/literature/shyama/FullText20.11/Annot_*.xml')

import io


def getfileblocks(file_path):
    subFileBlocks = []

    with io.open(file_path, 'r', encoding='utf8') as fh:
        for line in fh:
            if line.startswith('<!DOCTYPE'):
                subFileBlocks.append(line)
            else:
                subFileBlocks[-1] += line

    return subFileBlocks



def process_each_article(each_file_article):

    files_list = getfileblocks(each_file_article)
    article_chunks = [files_list[x:x+chunck_size] for x in range(0, len(files_list), chunck_size)]
    # Print files in seperate files
    for index, article in enumerate(article_chunks):
        with open(result_path + each_file_article.split('/')[-1][:-4]+'_split_'+str(index) + ".xml", "w") as text_file:
            text_file.writelines(article)



parser = argparse.ArgumentParser(description='This script will process patch files to split them into chunks of 100s')
parser.add_argument("-f", "--file", nargs=1, required=True, help="OTAR splitter XML", metavar="PATH")
args = parser.parse_args()

process_each_article(args.file[0])



