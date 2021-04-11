import logging
from lib.get_repo_info import get_top_repositories
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
    repos = get_top_repositories()
    logger.info(repos)
    static_typing_types = dir(typing)


if __name__ == "__main__":
    main()

