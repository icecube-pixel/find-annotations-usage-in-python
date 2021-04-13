import logging
import requests
from constants import _github_base_url, _language, _query_str, _language
import json
from typing import List, Tuple, Dict
import sys, os
import time
import pickle

logger = logging.getLogger(__name__)

headers = {"Accept": "application/vnd.github.v3+json"}

def get_top_repositories(args: Dict)->Tuple[List[str],int]:
    """
    Gets the top repositories based on 
        language python
        Desc Order based on stars of repo
    """
    logger.info("Inside get top repositories function")
    page_counter, per_page = 0, 100
    github_repo_data = check_if_files_present_on_disk()
    if len(github_repo_data) > 0:
        return github_repo_data, 200
    else:
        github_repo_data = []
        while True:  
            url = _github_base_url + requests.utils\
                    .quote(_query_str.substitute(PAGE=page_counter.__str__(),
                            PER_PAGE=per_page.__str__(), lang=_language))
            page_counter = page_counter + 1
            logger.info(url)
            response = requests.get(url, headers=headers, auth=(args['username'], args['password']))
            status_code = response.status_code
            if status_code == 200:
                data = response.json()
                epoch_nano_sec = str(round(time.time() * 100000))
                path_to_dump = os.path.join("data", epoch_nano_sec)
            
                with open(path_to_dump, 'wb') as handle: # Dumping the data to pickle 
                    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

                try:
                    github_repo_data = github_repo_data + [repo_data['html_url'] for repo_data in data['items']]
                except Exception as e:
                    logger.error("html_url is not found in response of the API")
                    return ['None'], status_code
            else:
                break
        return github_repo_data, status_code         
    

def check_if_files_present_on_disk()->Tuple[List[str],int]:
    """ Checks for pickle files that has saved response from github """
    file_names = os.listdir("data/")
    files_to_process = [os.path.join("data", file_name) for file_name in file_names if "." not in file_name]
    objects = []
    for file_to_process in files_to_process:
        with (open(file_to_process, "rb")) as openfile:
            try:
                data = pickle.load(openfile)
                objects = objects + [repo_data['html_url'] for repo_data in data['items']]
            except EOFError:
                break
    return objects