import unittest

from mangas.parsers import UraSundayTitlesParser, UraSundayEpisodeParser

SERIAL_URL = "https://urasunday.com/serial_title"
COMPLETE_URL = "https://urasunday.com/complete_title"


TITLE_IDS = ["1", "2", "3", "4"]


class UraSundayTitlesParserTest(unittest.TestCase):
    def test_parse_serial_titles(self):
        parser = UraSundayTitlesParser()
        titles = parser.parse(url=SERIAL_URL)

        assert titles

    def test_parse_complete_titles(self):
        parser = UraSundayTitlesParser()
        titles = parser.parse(url=COMPLETE_URL)

        assert titles

    def test_parse_episode(self):
        parser = UraSundayEpisodeParser()

        for title_id in TITLE_IDS:
            output = parser.parse(url=f"https://urasunday.com/title/{title_id}/")

            assert output is not None
            assert len(output.pages) > 0


if __name__ == "__main__":
    unittest.main()
