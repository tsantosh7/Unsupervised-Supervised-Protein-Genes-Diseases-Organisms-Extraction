# Code to parallel process OTAR json file to extract sentences and entities
# (c) EMBL-EBI, June 2019
#
# Started: 7 June 2019
# Updated: 9 August  2019

_author_ = 'Santosh Tirunagari'

import os
import pandas as pd
import glob
import json

import multiprocessing


colNames = ('pmcid', 'section', 't_start', 't_end', 'd_start', 'd_end', 'text')

file_path = '/home/stirunag/Work/OTAR dumps/'
all_files = glob.glob(file_path+'*split*')

result_folder = '/home/stirunag/Work/OTAR dumps/'

def process_each_split_to_extract_sentences(complete_file_path):
    with open(complete_file_path) as f:
        print(complete_file_path)
        for line in f:
            json_line = json.loads(line)
            pmc_id = json_line['evidence']['literature_ref']['lit_id']
            # print(pmc_id)
            try:
                for each_sentence in json_line['evidence']['literature_ref']['mined_sentences']:
                    section = each_sentence['section']
                    t_start = each_sentence['t_start']
                    t_end = each_sentence['t_end']
                    d_start = each_sentence['d_start']
                    d_end = each_sentence['d_end']
                    sentence = each_sentence['text'].encode('cp1252').decode('utf-8')

                    OTAR_info = [pmc_id, section, t_start, t_end, d_start, d_end, sentence]
                    OTAR_data = pd.DataFrame(columns=colNames)

                    OTAR_dict = dict(zip(colNames, OTAR_info))
                    OTAR_CSV = OTAR_data.append(OTAR_dict, ignore_index=True)

                    OTAR_CSV.to_csv(result_folder + 'OTAR_sentences.csv', encoding='utf-8', index=False, mode='a', header=False)

                    del OTAR_data  # Very important to delete or it will consume the memory
            except:
                continue


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=14)
    pool.map(process_each_split_to_extract_sentences, all_files)
    pool.close()
    pool.join()
    print('done')