import unittest
from teinfbot.utils.time import TimeUtils


class TestTimeUtils(unittest.TestCase):
    def testGetTimeDescFromMinutes(self):
        self.assertEqual(TimeUtils.getTimeDescFromMinutes(0), "0:00")
        self.assertEqual(TimeUtils.getTimeDescFromMinutes(10), "0:10")
        self.assertEqual(TimeUtils.getTimeDescFromMinutes(70), "1:10")
        self.assertEqual(TimeUtils.getTimeDescFromMinutes(2000), "1 dzień, 9:20")
        self.assertEqual(TimeUtils.getTimeDescFromMinutes(6996), "4 dni, 20:36")


if __name__ == '__main__':
    unittest.main()
