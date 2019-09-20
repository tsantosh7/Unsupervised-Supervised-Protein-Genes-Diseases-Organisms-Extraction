import wget
import zipfile
import requests
from bs4 import BeautifulSoup
import os
import multiprocessing

def run_process(url, output_path):
    wget.download(url, out=output_path)
    # TODO: you can write your rename logic at here using os.rename


if __name__ == '__main__':
    cpus = multiprocessing.cpu_count()
    max_pool_size = 4
    pool = multiprocessing.Pool(cpus if cpus < max_pool_size else max_pool_size)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target = '/home/santosh/Work/EPMC_xml_dumps/'
    xml_dumps_url = 'https://europepmc.org/ftp/oa/'
    download_list = []


    download_list.append([xml_dumps_url.format(n=name, p=prefix), path])

    for url, path in download_list: # change here to download other files
        print('Beginning file download with wget module {n}'.format(n=url))
        pool.apply_async(run_process, args=(url, path, ))
    # add your code here to download other files
    pool.close()
    pool.join()
    print("finish")