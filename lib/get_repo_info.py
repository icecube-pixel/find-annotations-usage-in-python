import logging
import requests
from constants import _github_base_url, _language, _query_str, _language
import json
from typing import List, Tuple, Dict
import sys, os
import time
import pickle
from github import Github

logger = logging.getLogger(__name__)

headers = {"Accept": "application/vnd.github.v3+json"}

def get_top_repositories(args: Dict)->Tuple[List[str],int]:
    """
    Gets the top repositories based on 
        language python
        Desc Order based on stars of repo
    """
    logger.info("Inside get top repositories function")
    github_repo_data = check_if_files_present_on_disk()
    if len(github_repo_data) > 0:
        return github_repo_data, 200
    else:
        github_repo_data = []
        try:
            g_obj = Github(args['username'], args['password'])
            result = g_obj.search_repositories(query)
            for repo in result:
                github_repo_data.append(repo.clone_url)
            epoch_nano_sec = str(round(time.time() * 100000))
            path_to_dump = os.path.join("data", epoch_nano_sec)
        
            with open(path_to_dump, 'wb') as handle: # Dumping the data to pickle 
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return github_repo_data, status_code         
        except Exception as e:
            logger.error("Exception occurred while calling search repo {error}".format(error=e))
            return ['None'], status_code
        

def check_if_files_present_on_disk()->Tuple[List[str],int]:
    """ Checks for pickle files that has saved response from github """
    file_names = os.listdir("data/")
    files_to_process = [os.path.join("data", file_name) for file_name in file_names if "." not in file_name]
    objects = []
    if len(files_to_process) > 0:
        for file_to_process in files_to_process:
            with (open(file_to_process, "rb")) as openfile:
                try:
                    data = pickle.load(openfile)
                    objects = objects + data
                except EOFError:
                    break
    return objects