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
        output = site.parse_all_comics()

        assert output is not None

    # /api/comics/{comic_id}.json
    def test_parse_comic(self):
        site = MangaCross()
        for comic_id in COMIC_IDS:
            output = site.parse_comic(comic_id)

            print(output.comic.title)

            assert output is not None

    # TODO: /api/comics/{comic_id}/{episode_id}.json
    # def test_parse_episode(self):

    # /comics/{comic_id}/{episode_id}/viewer.json
    def test_parse_episode_viewer(self):
        site = MangaCross()
        for comic_id in COMIC_IDS:
            for episode_id in EPISODE_IDS:
                output = site.parse_episode_viewer(comic_id, episode_id)

                print(output.comic.title, output.page_count)

                assert output is not None
                assert output.page_count == len(output.episode_pages)


if __name__ == "__main__":
    unittest.main()
