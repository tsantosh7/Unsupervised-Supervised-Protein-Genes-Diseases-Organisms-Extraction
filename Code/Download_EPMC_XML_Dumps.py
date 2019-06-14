import wget
import zipfile
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
    target = "NEWCODE"
    prefix_list = ["NWZV1WB", "AWU3JAD", "NW96MRD"]
    download_list = []
    name_list = list(range(1, 23))
    name_list.extend(["zoom_side", "zoom_sole", "zoom_side-thumb"])
    for prefix in prefix_list:
        path = os.path.join(base_dir, prefix)
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.isdir(path):
            exit()
        for name in name_list:
            download_list.append(['https://img2.tennis-warehouse.com/360/{p}/{n}.jpg'.format(n=name, p=prefix), path])

    for url, path in download_list: # change here to download other files
        print('Beginning file download with wget module {n}'.format(n=url))
        pool.apply_async(run_process, args=(url, path, ))
    # add your code here to download other files
    pool.close()
    pool.join()
    print("finish")