from typing import List, Dict
from bs4 import BeautifulSoup
import requests
import logging
import re, os
import subprocess
from time import sleep
from constants import sleep_counter
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)
temp_dir = "/tmp"

class ErrorWhileProcessingUrl(Exception):
    """ Throws this exception when any issue was encounterd while processing URL"""
    pass

@retry(stop=(stop_after_attempt(5)), wait=wait_exponential(multiplier=1, min=2, max=5))
def parse_html_using_bs(url : str)->BeautifulSoup:
    """ Gets the html using requests and parse using bs4"""
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    return soup


def get_typing_module_occurances_github(url: str)->int:
    """ Gets the occurance value from github instead of api.github """
    soup = parse_html_using_bs(url)
    for search_result in soup.find_all("h3"):
        if len(re.findall("code results", search_result.__str__())) > 0:
            split_results = search_result.__str__().split('code results')[0].split(" ")
            logger.info(split_results)
            for value in split_results:
                if value.isdigit():
                    return value
    return 0


@retry(stop=(stop_after_attempt(5)), wait=wait_exponential(multiplier=1, min=2, max=5))
def process_url_for_typing_module(url : str)->int:
    try:
        logger.info("Processing url {0}".format(url))
        count = get_typing_module_occurances_github(url)
        return count
    except Exception:
        raise ErrorWhileProcessingUrl
        

def check_if_typing_module_used(repo_links: List[str])->Dict:
    """Checks if typing module is present using github search"""
    logger.info("Getting if typing module is used")
    url_list = ["{repo_name}/search?q=typing".format(repo_name=link) for link in repo_links]
    logger.info(len(set(url_list)))
    occurances = {}
    for url in set(url_list):
        count = process_url_for_typing_module(url)
        org_url = url.replace('/search?q=typing', '')
        occurances[org_url] = count
        sleep(sleep_counter)
    return occurances


@retry(stop=(stop_after_attempt(5)), wait=wait_exponential(multiplier=1, min=2, max=5))
def download_repo(repo_link: str)->str:
    """ Downloads the repo to the disk """
    logger.info("Downloading repo {repo}".format(repo=repo_link))
    folder_name = repo_link.split("/")[-1]
    temp_dir_path = os.path.join(temp_dir, folder_name)
    bash_cmd = "git clone {repo} {temp_dir}".format(repo=repo_link, temp_dir=temp_dir_path)
    downloaded_repo = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    downloaded_repo.communicate()
    return temp_dir_path

