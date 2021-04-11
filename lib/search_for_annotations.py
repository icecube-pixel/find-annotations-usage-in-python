from typing import List, Dict
from bs4 import BeautifulSoup
import requests
import logging
import re

logger = logging.getLogger(__name__)


def get_typing_module_occurances_github(url: str)->int:
    """ Gets the occurance value from github instead of api.github """
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    for search_result in soup.find_all("h3"):
        if len(re.findall("code results", search_result.__str__())) > 0:
            split_results = search_result.__str__().split('code results')[0].split(" ")
            for value in split_results:
                if value.isdigit():
                    return value
    return 0


def check_if_typing_module_used(repo_links: List[str])->Dict:
    """Checks if typing module is present using github search"""
    logger.info("Getting if typing module is used")
    url_list = ["{repo_name}/search?q=typing".format(repo_name=link) for link in repo_links]
    occurances = {}
    for url in url_list:
        logger.info("Processing url {0}".format(url))
        count = get_typing_module_occurances_github(url)
        org_url = url.replace('/search?q=typing', '')
        occurances[org_url] = count
    logger.info(occurances)
    return occurances