# Parsing BING API
# Code inspired from Maria Christofi
# Santosh Tirunagari
#
# (c) EMBL-EBI, June 2019
#
# Started: 25 June 2019
# Updated: 25 June 2019

_author_ = 'Santosh Tirunagari'

import os
import requests
# from pprint import pprint
import pandas as pd

page_size = 8
page_count = 10
no_hits = 2
old_cursor_mark = -1
cursor_mark = 0

result_folder = '/home/santosh/Work/Unsupervised-Protein-Genes-Diseases-Extraction/Results/' #os.getcwd()+'/'+'Results/'

colNames = ('pmc_id', 'exact')
pmcid_exact_dict = {}


while cursor_mark-old_cursor_mark != 0:

    if page_count<=no_hits*page_size:

        url = 'https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByProvider?provider=' \
                 'OpenTargets&filter=1&format=JSON&cursorMark=' + str(cursor_mark) + '&pageSize='+str(page_size)

        r = requests.get(url)

        json_results = r.json()

        # pprint(json_results['articles'][0]['annotations'][0]['exact'])
        for each_article in json_results['articles']:
            pmcid = each_article['pmcid']

            try:
                for each_annotation in each_article['annotations']:
                    exact = each_annotation['exact']
                    exact_info = [pmcid, exact]
                    GD_data = pd.DataFrame(columns=colNames)
                    pmcid_exact_dict = dict(zip(colNames, exact_info))
                    GD_CSV = GD_data.append(pmcid_exact_dict, ignore_index=True)
                    GD_CSV.to_csv(result_folder+'GD_exacts.csv',
                                  encoding='utf-8', index=False, mode='a', header=False)
                    del GD_data  # Very important to delete or it will consume the memory
            except KeyError:
                pass

        next_cursor_mark = json_results['nextCursorMark']
        old_cursor_mark = cursor_mark
        cursor_mark = next_cursor_mark

        # print(str(cursor_mark) + '  ' + str(next_cursor_mark))

        page_count = page_count + page_size
        print(str(page_count))



