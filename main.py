import logging
from lib.github_utils import get_top_repositories
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
    get_top_repositories()
    static_typing_types = dir(typing)
    logger.info(static_typing_types)


if __name__ == "__main__":
    main()

