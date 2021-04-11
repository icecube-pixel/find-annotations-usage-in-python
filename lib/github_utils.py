import logging
import requests
from constants import _github_base_url, _language, _query_str
import json
from typing import List, Tuple
import sys

logger = logging.getLogger(__name__)

headers = {"Accept": "application/vnd.github.v3+json"}

def get_top_repositories()->Tuple[List[str],int]:
    """
    Gets the top repositories based on 
        language python
        Desc Order based on stars of repo
    """
    logger.info("Inside get top repositories function")    
    url = _github_base_url + requests.utils.quote(_query_str)
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code == 200:
        data = response.json()
        try:
            github_repo_data = [repo_data['html_url'] for repo_data in data['items']]
            return github_repo_data, status_code
        except Exception as e:
            logger.error("html_url is not found in response of the API")
            return ['None'], status_code            
    else:
        return ['None'], status_code
