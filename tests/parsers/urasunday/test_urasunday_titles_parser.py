import unittest

from mangas.parsers import UraSundayTitlesParser

SERIAL_URL = "https://urasunday.com/serial_title"
COMPLETE_URL = "https://urasunday.com/complete_title"


class UraSundayTitlesParserTest(unittest.TestCase):
    def test_parse_serial_titles(self):
        parser = UraSundayTitlesParser()
        titles = parser.parse(url=SERIAL_URL)

        assert titles

    def test_parse_complete_titles(self):
        parser = UraSundayTitlesParser()
        titles = parser.parse(url=COMPLETE_URL)

        assert titles


if __name__ == "__main__":
    unittest.main()
