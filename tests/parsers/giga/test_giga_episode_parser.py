import unittest

from mangas.parsers import GigaAtomParser, GigaEpisodeParser
from mangas.auth import FirefoxPC, AuthConfigMixin
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

auth = AuthConfigMixin(
    # 設定しないと403になることがある
    user_agent=FirefoxPC.user_agent,
)


class GigaEpisodeParserTest(unittest.TestCase):
    def test_parse_episode(self):
        for url in ATOM_TEST_URLS:
            atom_parser = GigaAtomParser(url=URLConfig.from_string(url))
            atom = atom_parser.parse()
            link = atom.entries[0].link
            assert link

            print(link)
            episode_parser = GigaEpisodeParser(url=link + ".json", auth=auth)

            episode = episode_parser.parse()
            print("title", episode.readable_product.title)
            assert episode


if __name__ == "__main__":
    unittest.main()
