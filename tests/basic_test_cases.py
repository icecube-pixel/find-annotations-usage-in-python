import unittest
from unittest.mock import patch, Mock
import getpass, os, sys
_user = getpass.getuser()
repo_absolute_path = "/home/{user}/find-annotations-usage-in-python".format(user=_user)
sys.path.append(repo_absolute_path)

from lib.github_utils import get_top_repositories

class TestSum(unittest.TestCase):

    def test_mock_github_repositories_api(self):
        """
        Mocking the github repostories API to get top python repos
        """
        mock_get_patcher = patch('github_utils.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code = 200)
        mock_get_patcher.stop()
        top_repo_links, status_code = get_top_repositories()
        self.assertEqual(status_code, 200)
        self.assertTrue(top_repo_links) # Checks if the list is empty

if __name__ == '__main__':
    unittest.main()