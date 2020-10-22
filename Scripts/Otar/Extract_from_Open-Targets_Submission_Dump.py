# Code to parallel process OTAR json file to extract sentences and entities
# (c) EMBL-EBI, June 2019
#
# Started: 7 June 2019
# Updated: 9 August  2019

_author_ = 'Santosh Tirunagari'

import os
import pandas as pd
# import glob
import json

# import sys

# import multiprocessing



import argparse



colNames = ('pmcid', 'section', 't_start', 't_end', 'd_start', 'd_end', 'text')
sent_colNames = ('text')

file_path = '/nfs/gns/literature/Santosh_Tirunagari/OTAR_DUMPS/'
# all_files = glob.glob(file_path+'*split*')

result_folder = '/nfs/gns/literature/Santosh_Tirunagari/OTAR_TEXT/'

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

                    with open(result_folder + 'OTAR_sentences.csv', 'a') as sent_file:
                        sent_file.writelines(sentence+'\n')

                    OTAR_info = [pmc_id, section, t_start, t_end, d_start, d_end, sentence]
                    OTAR_data = pd.DataFrame(columns=colNames)

                    OTAR_dict = dict(zip(colNames, OTAR_info))
                    OTAR_CSV = OTAR_data.append(OTAR_dict, ignore_index=True)

                    OTAR_CSV.to_csv(result_folder + 'OTAR_data.csv', sep='\t', encoding='utf-8', index=True, mode='a', header=False)

                    del OTAR_data  # Very important to delete or it will consume the memory

            except:
                continue


parser = argparse.ArgumentParser(description='This script will extract text from jsons files')
parser.add_argument("-f", "--file", nargs=1, required=True, help="json splits", metavar="PATH")
args = parser.parse_args()
process_each_split_to_extract_sentences(args.file[0])


# if __name__ == '__main__':
    # pool = multiprocessing.Pool(processes=32)
    # pool.map(process_each_split_to_extract_sentences, all_files)
    # pool.close()
    # pool.join()
    # print('done')
