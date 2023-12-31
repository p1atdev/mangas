import unittest

from mangas.parsers import GigaAtomParser
from mangas.url import URLConfig


ATOM_TEST_URLS = [
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

SERIES_ATOM_TEST_URLS = [
    "https://shonenjumpplus.com/atom/series/4856001361048451884",
    "https://pocket.shonenmagazine.com/atom/series/13933686331618251437",
    "https://magcomi.com/atom/series/10834108156763513460?free_only=1",
]


class GigaAtomParserTest(unittest.TestCase):
    def test_parse_root_atom(self):
        for url in ATOM_TEST_URLS:
            print(url)
            parser = GigaAtomParser()

            atom = parser.parse(url=url)

            assert atom.namespaces["giga"]

    def test_parse_series_atom(self):
        for url in SERIES_ATOM_TEST_URLS:
            series_atom_parser = GigaAtomParser()
            series = series_atom_parser.parse(url=url)
            print("title", series.feed.title)
            print("entries", series.entries)
            assert series


if __name__ == "__main__":
    unittest.main()
