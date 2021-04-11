import logging
from lib.get_repo_info import get_top_repositories
from lib.search_for_annotations import check_if_typing_module_used
import sys
import typing

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

def main():
    logger.info('Inside Main')
    repos,status_code = get_top_repositories()
    logger.info(type(repos))
    check_if_typing_module_used(repos)
    static_typing_types = dir(typing)


if __name__ == "__main__":
    main()

