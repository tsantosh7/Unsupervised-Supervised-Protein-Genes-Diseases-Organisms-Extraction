#!/usr/bin/env python
# coding: utf-8

# In[64]:

import itertools 
import pandas as pd
import requests
import pandas as pd
from tqdm import tqdm
import time
import re
from ast import literal_eval as eval_list


all_dataset = pd.read_csv('CD_GP_DS_OG.csv', header=None, names = ['text', 'ner'])

def clean_Nones(ner_tags_):
    
    ner_tags = []
    clean_tags = []
        # had to do this as the position of entity tag and entity are exchanged in CD
    for each_ner_tag in ner_tags_:
        if 'CD' in each_ner_tag[3]:
            ner_tags.append([each_ner_tag[0], each_ner_tag[1], each_ner_tag[3], each_ner_tag[2]])
        else:
            ner_tags.append(each_ner_tag)
            

    ner_tags = sorted(ner_tags, key=lambda x: len(x[3]), reverse=True)
    if len(ner_tags)==1 and 'None' in ner_tags:
        return ner_tags
    elif len(ner_tags)>1 and 'None' in ner_tags:
        ner_tags.remove('None')
        return ner_tags
    else:
        return ner_tags
    
    
def remove_overlap(annotation_list):
    # first map each item to another item in the list
    mapped_list = list(itertools.combinations(clean_ner_tags, 2))
    unique_maplist = []
    for each_list in mapped_list:
        if each_list[0][2] !=each_list[1][2] and each_list[1][2]== 'CD':
            unique_maplist.append((each_list[0], each_list[1]))

#   now check for the overlaps
    overlapped_tags = []

    for each_map_list in unique_maplist:
        st_1_sp = each_map_list[0][0]
        en_1_sp = each_map_list[0][1]

        st_2_sp = each_map_list[1][0]
        en_2_sp = each_map_list[1][1]

        if st_1_sp <= st_2_sp <= en_1_sp and st_1_sp <= en_2_sp <= en_1_sp:
            if each_map_list[1][3] in each_map_list[0][3]: # process only if the CD is in otherwise not
                overlapped_tags.append(each_map_list[1])
                
#   get the final tags after removing the duplicates

    final_tags = []
    for each_ner_tag in clean_ner_tags:
        if each_ner_tag in overlapped_tags:
            pass
        else:
            final_tags.append(each_ner_tag)
            
    return final_tags



all_dataset.iloc[43]['ner']
clean_ner_tags = clean_Nones(eval_list(all_dataset.iloc[131]['ner']))




