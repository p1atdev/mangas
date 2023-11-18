import unittest

from mangas.parsers import GigaParser

TEST_URLS = [
    "https://shonenjumpplus.com/atom",
    "https://tonarinoyj.jp/atom",
    "https://viewer.heros-web.com/atom",
    "https://comicbushi-web.com/atom",
    "https://comicborder.com/atom",
    "https://comic-days.com/atom",
    "https://comic-action.com/atom",
    "https://comic-ogyaaa.com/atom",
    "https://comic-gardo.com/atom",
    "https://comic-zenon.com/atom",
    "https://feelweb.jp/atom",
    "https://kuragebunch.com/atom",
    "https://www.sunday-webry.com/atom",
    "https://magcomi.com/atom",
    "https://pocket.shonenmagazine.com/atom",
]


class GigaParserTest(unittest.TestCase):
    def test_init_parser(self):
        for url in TEST_URLS:
            print(url)
            parser = GigaParser(url=url)
            try:
                atom = parser.parse()
                self.assertIsNotNone(atom.namespaces["giga"])
            except Exception as e:
                print(e)


if __name__ == "__main__":
    unittest.main()
