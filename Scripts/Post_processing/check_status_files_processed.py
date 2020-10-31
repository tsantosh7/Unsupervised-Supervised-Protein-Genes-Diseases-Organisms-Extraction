# Code to check the status of the files being processed
# (c) EMBL-EBI
#
# Started: 20 October  2020
# Updated: 20 October  2020

_author_ = 'Santosh Tirunagari'

import os
import pandas as pd
import glob
import json

import sys

import multiprocessing



colNames = ('pmc_id', 'sent_id', 'text', 'ner', 'rel')

file_path = '/nfs/gns/literature/yangx/gitrepo/biobertepmc/ai_capo_logs/LSF_logs/' #/nfs/production/literature/Santosh_Tirunagari/logs/'
all_files = glob.glob(file_path+'error*')


for each_file in all_files:
    with open(each_file, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
	print(files_processed,time_taken)        
	#split_last_line = last_line.split('| ')
        #files_processed = split_last_line[1].split('/')[0]
        #time_taken = split_last_line[2].split('<')[0].replace('[','')
        #print(files_processed,time_taken)
