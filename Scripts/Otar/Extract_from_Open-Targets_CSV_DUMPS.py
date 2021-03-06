# Code to parallel process OTAR json file to extract sentences and entities
# (c) EMBL-EBI, June 2019
#
# Started: 12 June 2019
# Updated: 13 August  2019

_author_ = 'Santosh Tirunagari'

import os
import pandas as pd
import argparse
import re


colNames = ('pmcid', 'section', 't_start', 't_end', 'd_start', 'd_end', 'text')

# file_path = '/nfs/gns/literature/Santosh_Tirunagari/OTAR_DUMPS/OTAR_CSV_TEXT'
result_folder = '/nfs/gns/literature/Santosh_Tirunagari/Dataset/'

def process_each_split_to_extract_sentences(complete_file_path):
    OTAR_df = pd.read_csv(complete_file_path, names=colNames, encoding='utf-8')
    f_name = complete_file_path.split('/')[-1]
    for index, row in OTAR_df.iterrows():
        sentence_list = []
        for each_word in row['text'].split():
            try:
                sentence_list.append(
                    each_word.encode('latin_1').decode('utf-8').strip())  # Each char is a Unicode codepoint.
            except:
                sentence_list.append(re.sub(r'[^\x00-\x7f]', r'', each_word).strip())

        sentence = ' '.join(sentence_list)

        with open(result_folder + f_name+ '.csv', 'a') as sent_file:
            sent_file.writelines(sentence+'\n')


parser = argparse.ArgumentParser(description='This script will extract text from jsons files')
parser.add_argument("-f", "--file", nargs=1, required=True, help="CSV splits", metavar="PATH")
args = parser.parse_args()
process_each_split_to_extract_sentences(args.file[0])
