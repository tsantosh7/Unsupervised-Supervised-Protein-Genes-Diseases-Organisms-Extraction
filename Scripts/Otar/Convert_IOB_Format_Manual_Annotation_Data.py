# Code to parallel process OTAR json file to extract sentences and entities
# (c) EMBL-EBI, June 2019
#
# Started: 9 Septmember  2019
# Updated: 9 Septmember  2019

_author_ = 'Santosh Tirunagari'

import os
import pandas as pd
import glob
import json

import sys

import multiprocessing



# import argparse



colNames = ('pmc_id', 'sent_id', 'text', 'ner', 'rel')

file_path = '/mnt/droplet/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/'
all_files = glob.glob(file_path+'*fulltext_batch*')
result_folder = '/mnt/droplet/nfs/gns/literature/Santosh_Tirunagari/EBI standard Dataset/CSV/'


def process_each_split_to_extract_sentences(complete_file_path):
    with open(complete_file_path) as json_file_ner_rel:
        print(complete_file_path)
        json_data = json.loads(json_file_ner_rel.read())

    for articles in json_data:
        pmc_id = articles #json_data[articles]
        for each_annotation in json_data[articles]['annotations']:
            try:
                text = each_annotation['sent'].encode('utf-8').decode('utf-8')
                if(each_annotation['rel'] == None):
                    label = 'NGD'
                else:
                    label = 'YGD'

                if(each_annotation['ner'] == None):
                    ner = 'No-Ner'
                else:
                    ner = each_annotation['ner']

                sent_id = each_annotation['sid']

                exact_info = [pmc_id, sent_id, text, ner, label]
                GD_data = pd.DataFrame(columns=colNames)
                pmcid_exact_dict = dict(zip(colNames, exact_info))
                GD_CSV = GD_data.append(pmcid_exact_dict, ignore_index=True)
                GD_CSV.to_csv(result_folder + 'manual_annot_exacts_180.csv',
                              encoding='utf-8', index=False, mode='a', header=False, sep='\t')
                del GD_data  # Very important to delete or it will consume the memory

            except KeyError:
                pass


# parser = argparse.ArgumentParser(description='This script will extract text from jsons files')
# parser.add_argument("-f", "--file", nargs=1, required=True, help="json splits", metavar="PATH")
# args = parser.parse_args()
# process_each_split_to_extract_sentences(args.file[0])


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=8)
    pool.map(process_each_split_to_extract_sentences, all_files)
    pool.close()
    pool.join()
    print('done')
