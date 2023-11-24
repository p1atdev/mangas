import unittest

from mangas.websites import MangaCross

COMIC_IDS = [
    "fairway",
    "watamaho",
    "kimigaro",
    "okaeri",
]

EPISODE_IDS = range(1, 3)


class MangaCrossTest(unittest.TestCase):
    def test_init_website(self):
        site = MangaCross()

        assert site.url.compose() == "https://mangacross.jp"

    # /api/comics.json
    def test_parse_all_comics(self):
        site = MangaCross()
        output = site.parse_comics()

        assert output is not None

    # /api/comics/{comic_id}.json
    def test_parse_series(self):
        site = MangaCross()
        for comic_id in COMIC_IDS:
            output = site.parse_series(comic_id)

            print(output.comic.title)

            assert output is not None

    # TODO: /api/comics/{comic_id}/{episode_id}.json
    # def test_parse_episode(self):

    # /comics/{comic_id}/{episode_id}/viewer.json
    def test_parse_episode_viewer(self):
        site = MangaCross()
        for comic_id in COMIC_IDS:
            for episode_id in EPISODE_IDS:
                output = site.parse_episode(comic_id, episode_id)

                print(output.comic.title, output.page_count)

                assert output is not None
                assert output.page_count == len(output.episode_pages)

    def test_parse_comic_id(self):
        site = MangaCross()
        for comic_id in COMIC_IDS:
            url = f"https://mangacross.jp/comics/{comic_id}"
            output = site._parse_comic_id(url)

            assert output == comic_id

            url_long = f"https://mangacross.jp/comics/{comic_id}/1/viewer.json"
            output_long = site._parse_comic_id(url_long)

            assert output_long == comic_id

    def test_parse_episode_id(self):
        site = MangaCross()
        for comic_id in COMIC_IDS:
            for episode_id in EPISODE_IDS:
                url = f"https://mangacross.jp/comics/{comic_id}/{episode_id}"
                output = site._parse_episode_id(url)

                assert output == str(episode_id)

                url_long = (
                    f"https://mangacross.jp/comics/{comic_id}/{episode_id}/viewer.json"
                )
                output_long = site._parse_episode_id(url_long)

                assert output_long == str(episode_id)


if __name__ == "__main__":
    unittest.main()
