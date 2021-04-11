import logging
from lib.get_repo_info import get_top_repositories
from lib.search_for_annotations import check_if_typing_module_used
from lib.search_for_annotations import download_repo
import sys
import typing
import json
import subprocess
import re, os
from typing import List
import pandas as pd
import shutil

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

def read_key_words_from_files()->List[str]:
    """ Preparing a list to search on repo """
    file_names = os.listdir('data/')
    key_words_to_search = []
    for file_name in file_names:
        logger.info("Processing file : {file}".format(file=file_name))
        f = open(os.path.join('data', file_name))
        data = json.load(f)
        key_words_to_search = key_words_to_search + data['types']
    return key_words_to_search


def main():
    logger.info('Inside Main')
    repos,status_code = get_top_repositories()
    instances_found_per_repo = check_if_typing_module_used(repos)
    repos_to_download = [ key for key, value in instances_found_per_repo.items() if int(value) > 0]
    logger.info(repos_to_download)
    keys_to_search = read_key_words_from_files()
    logger.info(keys_to_search)
    master_data = []
    for repo_url in repos_to_download:
        temp_dir_path = download_repo(repo_url)
        resultant_dict = {}
        for key in keys_to_search:
            bash_cmd = 'grep -are {key} {temp_path} | grep -E "\->\s{key}|\[{key}|:\s{key}" | grep ".py" | wc -l'.format(key=key, temp_path=temp_dir_path)
            bash_process = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
            lines_to_iterate = bash_process.stdout.readlines()
            value = lines_to_iterate[0].decode("utf-8").replace('\n', '')
            resultant_dict[key] = value.__int__()
        resultant_dict['repo_url'] = repo_url
        master_data.append(resultant_dict)
        shutil.rmtree(temp_dir_path)
        

if __name__ == "__main__":
    main()

