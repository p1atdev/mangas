import unittest

from mangas.websites import UraSunday

TITLE_IDS = ["1301", "2060"]


class UraSundayWebsiteTest(unittest.TestCase):
    def test_init_website(self):
        site = UraSunday()

        assert site.url.compose() == "https://urasunday.com"

    def test_parse_episode(self):
        site = UraSunday()

        for title_id in TITLE_IDS:
            output = site.parse_episode(title_id)

            print(output.title_name, output.episode_name)

            assert output is not None

    def test_parse_title_id(self):
        site = UraSunday()

        for title_id in TITLE_IDS:
            url = f"https://urasunday.com/title/{title_id}"
            output = site._parse_title_id(url)

            assert output == title_id

        for title_id in TITLE_IDS:
            url = f"https://urasunday.com/title/{title_id}/"
            output = site._parse_title_id(url)

            assert output == title_id

        for title_id in TITLE_IDS:
            url = f"https://urasunday.com/title/{title_id}/1234"
            output = site._parse_title_id(url)

            assert output == title_id

    def test_parse_titles(self):
        site = UraSunday()

        output = site.parse_titles("/serial_title")

        assert len(output.titles) > 0

        print(output.titles[0].url)

    def test_parse_serial_titles(self):
        site = UraSunday()

        output = site.parse_serial_titles()

        assert len(output.titles) > 0

        print(output.titles[0].url)

    def test_parse_complete_titles(self):
        site = UraSunday()

        output = site.parse_complete_titles()

        assert len(output.titles) > 0

        print(output.titles[0].url)
