#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import pandas as pd
from tqdm import tqdm
import time
import re
import ast




def get_GP_DS_OG(sentences):
    
    queryurl = 'http://ai-capo-api-1:5001/predict/sent'
    header = {"Content-type": "application/json"} 
    
    post_fields_capo2 = {"text": sentence}
    

    response = requests.post(queryurl, json=post_fields_capo2, headers=header)

    if response.status_code==200:
        annotations = response.json()['annotations'] #ast.literal_eval()
    else:
        annotations = ''
    
    return annotations




file_path = '/nfs/gns/literature/Santosh_Tirunagari/Merge_CD-GP-DS-OG/GP_CSV_formats/'
dataset = pd.read_csv(file_path+'test.csv', sep = '\t', names = ['pmcid', 'text', 'ner'])

colNames = ['text', 'ner']

for iter_, row in tqdm(dataset.iterrows(), total = len(dataset)):
    
    sector_dict =[]
    sector_data = pd.DataFrame(columns=colNames)
    
    sentence = row['text']
    try:
        ner = ner = ast.literal_eval(row['ner'])
    except ValueError:
        ner = ['None']
            
    annotations = get_GP_DS_OG(sentence)
    new_ner =ner+annotations
    


    sector_dict.append(dict(zip(colNames, [sentence,new_ner])))
    sector_CSV = sector_data.append(sector_dict, ignore_index=True)

    sector_CSV.to_csv(file_path+'CD_GP_DS_OG_test.csv',encoding='utf-8', index=False,  mode='a', header=False)
    del sector_data # Very important to delete or it will consume the memory





