import unittest
from teinfbot.utils.meme import Meme

class TestMeme(unittest.TestCase):
    def testGetMeme(self):

        # zdjęcie
        meme = Meme.get_meme('https://jbzd.com.pl/obr/1787202/doktorspiele')
        self.assertEqual(meme.title, 'DOKTORSPIELE')
        self.assertEqual(meme.url, 'https://jbzd.com.pl/obr/1787202/doktorspiele')
        self.assertEqual(meme.image_url, 'https://i1.jbzd.com.pl/contents/2021/03/normal/GX4ajnhIWKEIo0jFTBKtiIiUJzkGw3TQ.jpg')
        self.assertEqual(meme.tags, ['#humor', '#meme', '#dowcipy', '#screen'])
        self.assertIsNotNone(meme.votes)

        # video
        meme = Meme.get_meme('https://jbzd.com.pl/obr/1787449/rosnie-mlody-gangster-xd')
        self.assertEqual(meme.title, 'Rośnie młody gangster xD')
        self.assertEqual(meme.url, 'https://jbzd.com.pl/obr/1787449/rosnie-mlody-gangster-xd')
        self.assertEqual(meme.image_url, 'https://i1.jbzd.com.pl/contents/2021/03/RRb4Wi4rFQycyLL9uzKmN0NAh9Lna3wg.mp4')
        self.assertEqual(meme.tags, ['#zabawa', '#dzieciaki', '#humor', '#gangster',  '#video'])
        self.assertIsNotNone(meme.votes)

    def testRandomMeme(self):

        for i in range(1, 3):
            meme = Meme.random_meme(i)
            self.assertIsNotNone(meme.title)
            self.assertIsNotNone(meme.url)
            self.assertIsNotNone(meme.image_url)
            self.assertIsNotNone(meme.tags)


if __name__ == '__main__':
    unittest.main()
