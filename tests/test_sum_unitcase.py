import unittest
# import sys

# sys.path.append("")
from src.sum import for_loop_sum

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(for_loop_sum([1,2,3]),6)


if __name__ == '__main__':
    unittest.main()