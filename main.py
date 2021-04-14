import logging
from lib.get_repo_info import get_top_repositories
from lib.search_for_annotations import check_if_typing_module_used
from lib.search_for_annotations import download_repo
import sys
import typing
import json
import subprocess
import re, os
from typing import List, Dict
import pandas as pd
import shutil
import numpy as np
import argparse

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
        if '.json' not in file_name:
            continue
        logger.info("Processing file : {file}".format(file=file_name))
        f = open(os.path.join('data', file_name))
        data = json.load(f)
        key_words_to_search = key_words_to_search + data['types']
    return key_words_to_search


def get_inputs()->Dict:
    """Gets the username and password from the console """
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", dest="token", help="Enter the oAuth token", required=True) 
    args = vars(parser.parse_args())
    return args


def main():
    logger.info('Inside Main')
    args = get_inputs()
    repos,status_code = get_top_repositories(args)
    instances_found_per_repo = check_if_typing_module_used(repos)
    repos_to_download = [ key for key, value in instances_found_per_repo.items() if int(value) > 0]
    logger.info(repos_to_download)
    keys_to_search = read_key_words_from_files()
    logger.info(keys_to_search)
    master_data = []
    for repo_url in repos_to_download:
        temp_dir_path = download_repo(repo_url)
        try:
            resultant_dict = {}
            for key in keys_to_search:
                bash_cmd = 'grep -are {key} {temp_path} | grep -E "\->\s{key}|\[{key}|:\s{key}" | grep ".py" | wc -l'.format(key=key, temp_path=temp_dir_path)
                bash_process = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
                lines_to_iterate = bash_process.stdout.readlines()
                value = lines_to_iterate[0].decode("utf-8").replace('\n', '')
                resultant_dict[key] = value
            resultant_dict['repo_url'] = repo_url
            master_data.append(resultant_dict)
        except Exception as e:
            logger.error(e)
        finally:
            shutil.rmtree(temp_dir_path)
    df_with_data = pd.DataFrame(master_data)    
    fill_repos = list(set(instances_found_per_repo.keys()) - set(repos_to_download))
    rows, cols = len(fill_repos) , len(df_with_data.columns.tolist()) - 1
    col_names = df_with_data.columns.tolist()
    col_names.remove('repo_url')
    df_zeros = pd.DataFrame(np.zeros((rows, cols)), columns=col_names)
    df_zeros['repo_url'] = fill_repos
    df = pd.concat([df_with_data, df_zeros])
    df.to_csv('data/Pattern_count_across_repos.csv', index=False)


if __name__ == "__main__":
    main()

# curl -G https://api.github.com/search/repositories?q=python%20language%3Apython%26sort%3Dstars%26order%3Ddesc -H "application/vnd.github.v3+json" | jq ".items[] | {name, description, language, watchers_count, html_url} | length" | wc -l 
# TODO Need to use per_page and page. Refer to https://docs.github.com/en/rest/reference/search#search-repositories