from typing import List, Dict
from bs4 import BeautifulSoup
import requests
import logging
import re, os
import subprocess

logger = logging.getLogger(__name__)
temp_dir = "/tmp"

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
    for index, url in enumerate(url_list):
        if index > 5:
            break
        logger.info("Processing url {0}".format(url))
        count = get_typing_module_occurances_github(url)
        org_url = url.replace('/search?q=typing', '')
        occurances[org_url] = count
    logger.info(occurances)
    return occurances


def download_repo(repo_link: str)->str:
    """ Downloads the repo to the disk """
    logger.info("Downloading repo {repo}".format(repo=repo_link))
    folder_name = repo_link.split("/")[-1]
    temp_dir_path = os.path.join(temp_dir, folder_name)
    bash_cmd = "git clone {repo} {temp_dir}".format(repo=repo_link, temp_dir=temp_dir_path)
    downloaded_repo = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    downloaded_repo.communicate()
    return temp_dir_path


def grep_for_patterns(repo_path:str):
    """
    Greps for patterns
    """
    return