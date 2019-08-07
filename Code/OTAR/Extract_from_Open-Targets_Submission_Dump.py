# (c) EMBL-EBI, June 2019
#
# Started: 25 June 2019
# Updated: 5 August  2019

_author_ = 'Santosh Tirunagari'

import os
# from pprint import pprint
import pandas as pd

import json


colNames = ('pmcid', 'section', 't_start', 't_end', 'd_start', 'd_end', 'text')
pmcid_exact_dict = {}



file_path = '/home/stirunag/Work/OTAR dumps/cttv025-24-05-2019.json'

# file_path = '/home/stirunag/Work/OTAR dumps/toy_data.txt'
result_folder = '/home/stirunag/Work/OTAR dumps/'

with open(file_path) as f:
    for line in f:
        json_line = json.loads(line)
        pmc_id = json_line['evidence']['literature_ref']['lit_id']
        for each_sentence in json_line['evidence']['literature_ref']['mined_sentences']:
            section = each_sentence['section']
            t_start = each_sentence['t_start']
            t_end = each_sentence['t_end']
            d_start = each_sentence['d_start']
            d_end = each_sentence['d_end']
            sentence = each_sentence['text']

            OTAR_info = [pmc_id, section, t_start, t_end, d_start, d_end, sentence]
            OTAR_data = pd.DataFrame(columns=colNames)

            OTAR_dict = dict(zip(colNames, OTAR_info))
            OTAR_CSV = OTAR_data.append(OTAR_dict, ignore_index=True)

            OTAR_CSV.to_csv(result_folder + 'OTAR_sentences.csv', encoding='utf-8', index=False, mode='a', header=False)

            del OTAR_data  # Very important to delete or it will consume the memory


