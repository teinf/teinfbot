import unittest
from teinfbot.utils.levels import LevelsUtils


class TestLevelsUtils(unittest.TestCase):
    def testLevelsUtils(self):
        for i in range(15):
            level = LevelsUtils.levelFromExp(10**i)
            self.assertEqual(level, LevelsUtils.levelFromExp(LevelsUtils.expFromLevel(level)))



if __name__ == '__main__':
    unittest.main()
