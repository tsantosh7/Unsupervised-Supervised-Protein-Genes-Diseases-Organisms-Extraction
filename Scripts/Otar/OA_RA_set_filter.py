#!/usr/bin/env python
# coding: utf-8

# This script will process patch files to get OA and RA articles only
# (c) EMBL-EBI, Jan 2020
#
# Started: 15 Nov 2020
# Updated: 30 Nov  2020


import argparse
import glob
from tqdm import tqdm
import sys
import pathlib
import csv
import argparse
import pandas as pd
import json
import io


# Read IDS OAs and RAs  Not usefu now. Use this when working at EuropePMC level
id_database_df= pd.read_csv('/nfs/misc/literature/Santosh_Tirunagari/OTAR_ids_dataset/id_dataset.csv')
FT_IDS = dict(zip(id_database_df['FT_ID'].values.tolist(), id_database_df['PUB_DATE'].values))
# id_database_df.sample(n=2)


def process_each_file_in_job(each_file_path):
    p = pathlib.Path(each_file_path)

    if 'NMP_FT20.09' in each_file_path:
        result_path = '/nfs/production/literature/Santosh_Tirunagari/OA_RAset/NMP_FT20.09/'
    elif 'NDP_FT20.09' in each_file_path:
        result_path = '/nfs/production/literature/Santosh_Tirunagari/OA_RAset/NDP_FT20.09/'
    else:
        result_path = '/nfs/production/literature/Santosh_Tirunagari/OA_RAset/'

    with io.open(each_file_path, 'r', encoding='utf8') as f:
        json_content = f.readlines()

    with open(result_path + p.name, 'at', encoding='utf8') as json_file:
        for each_json_file in tqdm(json_content):
            file_json = json.loads(each_json_file)
            if file_json['pmid'] in FT_IDS:
                json.dump(file_json, json_file, ensure_ascii=False)
                json_file.write('\n')


parser = argparse.ArgumentParser(description='This script will extract OA and RA articles only')
parser.add_argument("-f", "--file", nargs=1, required=True, help="OTAR New Pipeline OA RA Jsonl filter", metavar="PATH")
args = parser.parse_args()

process_each_file_in_job(args.file[0])




