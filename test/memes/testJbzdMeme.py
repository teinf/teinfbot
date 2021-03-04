import unittest
from teinfbot.utils.memes import JbzdMeme

class TestMeme(unittest.TestCase):
    def testGetMeme(self):

        # zdjęcie
        meme = JbzdMeme.get_meme('https://jbzd.com.pl/obr/1787202/doktorspiele')
        self.assertEqual(meme.title, 'DOKTORSPIELE')
        self.assertEqual(meme.url, 'https://jbzd.com.pl/obr/1787202/doktorspiele')
        self.assertEqual(meme.image_url, 'https://i1.jbzd.com.pl/contents/2021/03/normal/GX4ajnhIWKEIo0jFTBKtiIiUJzkGw3TQ.jpg')
        self.assertEqual(meme.tags, ['#humor', '#meme', '#dowcipy', '#screen'])

        # video
        meme = JbzdMeme.get_meme('https://jbzd.com.pl/obr/1787449/rosnie-mlody-gangster-xd')
        self.assertEqual(meme.title, 'Rośnie młody gangster xD')
        self.assertEqual(meme.url, 'https://jbzd.com.pl/obr/1787449/rosnie-mlody-gangster-xd')
        self.assertEqual(meme.image_url, 'https://i1.jbzd.com.pl/contents/2021/03/RRb4Wi4rFQycyLL9uzKmN0NAh9Lna3wg.mp4')
        self.assertEqual(meme.tags, ['#zabawa', '#dzieciaki', '#humor', '#gangster',  '#video'])

    def testRandomMeme(self):

        for i in range(5):
            meme = JbzdMeme.random_meme()
            self.assertIsNotNone(meme.title)
            self.assertIsNotNone(meme.url)
            self.assertIsNotNone(meme.image_url)
            self.assertIsNotNone(meme.tags)


if __name__ == '__main__':
    unittest.main()
