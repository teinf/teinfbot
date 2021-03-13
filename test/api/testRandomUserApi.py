import unittest
from teinfbot.utils.api.random_user import RandomUserApi, User

class TestRandomUserApi(unittest.TestCase):
    def testGetRandomUser(self):
        random_user = RandomUserApi.get_random_user()
        self.assertIsNotNone(random_user)

if __name__ == '__main__':
    unittest.main()
