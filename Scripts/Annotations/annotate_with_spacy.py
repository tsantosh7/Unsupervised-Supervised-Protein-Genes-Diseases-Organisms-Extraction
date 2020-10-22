import glob
import gzip
from bs4 import BeautifulSoup
import lxml
from collections import defaultdict
from tqdm import tqdm
import requests
import random
import sys
from bsub import bsub
import multiprocessing
from fuzzywuzzy import fuzz


def getfileblocks(file_path):
    subFileBlocks = []

    with gzip.open(file_path, 'rt') as fh:
        for line in fh:
            if line.startswith('<!DOCTYPE article'):
                subFileBlocks.append(line)
            else:
                subFileBlocks[-1] += line

    return subFileBlocks


def GP_soup(file_soup):
    dict_sentences = defaultdict(list)
    for each_ztag in file_soup.find_all('z:uniprot'):
        try:
            gene_sentence = each_ztag.findParents('plain')[0].text
            dict_sentences[gene_sentence].append(each_ztag)
        except:
            pass
    return dict_sentences


def compare_with_ml_annotations(r, z_tags, ml_json):
    FP_removed_z_tags = []
    for each_z_tag in z_tags:
        for each_ml_annotation in r.json()['annotations']:
            score = fuzz.token_set_ratio(each_ml_annotation[3], each_z_tag.text)
            if score == 100 and each_ml_annotation[2] == 'GP':
                FP_removed_z_tags.append(each_z_tag)

    return list(set(z_tags) - set(FP_removed_z_tags))


def get_unique_fp_tags(GP_dict_sentences):

    url = 'http://ai-capo-api-lb/spaCy_ner_predictor?text_sentence='  # Load Balancer

    FP_dict_sentences = defaultdict(list)
    set_FPs = set()

    for each_uniprot_sentence, z_tags in GP_dict_sentences.items():
        r = requests.get(url + each_uniprot_sentence)
        if r.status_code == 200 and r.json()['status'] == 200:
            FPs = compare_with_ml_annotations(r, z_tags, r.json())
            if FPs:
                FP_dict_sentences[each_uniprot_sentence].append(FPs)
        # else:
            # print(each_uniprot_sentence)

    for FP_sent, FP_tag in FP_dict_sentences.items():
        for each_ztag in FP_tag[0]:
            set_FPs.add(each_ztag)

    return list(set_FPs)




# for each_file_content in subFileBlocks:


def process_each_file_in_job(each_file_path):

    path_new = '/mnt/droplet/nfs/gns/literature/machine-learning/Santosh/fp_removed_patches/'
    ss = getfileblocks(each_file_path)
    for each_article in tqdm(ss):
        soup = BeautifulSoup(each_article, 'xml')
        GP_dict_sentences = GP_soup(soup)
        if GP_dict_sentences:
            unique_fps = get_unique_fp_tags(GP_dict_sentences)

            for each_fp in unique_fps:
                for tag in soup.findAll('z:uniprot', attrs={'ids':each_fp['ids']}):
                    tag.unwrap()

            new_file_content = str(soup).replace('<?xml version="1.0" encoding="utf-8"?>\n','').replace('</ebiroot>','</ebiroot>\n')

            with gzip.open(path_new+'edited_'+each_file_path.split('/')[-1], 'at') as f:
                f.write(new_file_content)



full_text_path = '/mnt/droplet/nfs/gns/literature/rdf_annotation_data/daily_pipeline_api/15_08_1947/fulltext/'  # job_1/annotation/'
all_jobs_path = sorted(glob.glob(full_text_path + 'job_*'))

xml_annotation_path = []
for each_job_path in all_jobs_path:
    xml_annotation_path.extend(sorted(glob.glob(each_job_path + '/annotation/' + '*.xml.gz')))



if __name__ == '__main__':
    xml_annotation_path_ = xml_annotation_path[0:1]
    # pool = multiprocessing.Pool(processes=32)
    # pool.map(process_each_file_in_job, xml_annotation_path_)
    # pool.close()
    # pool.join()
    # print('done')

    sub = bsub("some_job", R="rusage[mem=1]", verbose=True)