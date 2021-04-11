import logging
from lib.github_utils import get_top_repositories
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

def main():
    logger.info('Inside Main')
    get_top_repositories()


if __name__ == "__main__":
    main()

