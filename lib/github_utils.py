import logging
import requests
from constants import _github_base_url, _language, _query_str
import json
from typing import List, Union
import sys

logger = logging.getLogger(__name__)

headers = {"Accept": "application/vnd.github.v3+json"}

def get_top_repositories()->List[str]:
    """
    Gets the top repositories based on 
        language python
        Desc Order based on stars of repo
    """
    logger.info("Inside get top repositories function")    
    url = _github_base_url + requests.utils.quote(_query_str)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        github_repo_data = [repo_data['html_url'] for repo_data in data['items']]
        logger.info(github_repo_data)
        return github_repo_data
    else:
        return ['None']
