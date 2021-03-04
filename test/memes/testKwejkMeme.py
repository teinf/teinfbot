import unittest

from teinfbot.utils.memes import KwejkMeme


class MyTestCase(unittest.TestCase):
    def test_get_meme(self):
        url = 'https://kwejk.pl/zobacz/3718987/sczescie.html'
        meme = KwejkMeme.get_meme(url)

        self.assertEqual(meme.title, 'sczęście')
        self.assertEqual(meme.url, url)
        self.assertEqual(meme.image_url, 'https://i1.kwejk.pl/k/obrazki/2021/02/8lmvVnB6iiBacSCL.jpg')
        self.assertEqual(meme.tags, ['#obrazek'])

    def test_random_meme(self):

        for i in range(5):
            meme = KwejkMeme.random_meme()

            self.assertIsNotNone(meme.title)
            self.assertIsNotNone(meme.url)
            self.assertIsNotNone(meme.image_url)
            self.assertIsNotNone(meme.tags)



if __name__ == '__main__':
    unittest.main()
