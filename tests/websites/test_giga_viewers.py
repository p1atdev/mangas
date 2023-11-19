import unittest

from mangas.websites import ShonenJumpPlus, HerosWeb, TonariNoYoungJump


TEST_CASES = [
    {
        "class": ShonenJumpPlus,
        "url": "https://shonenjumpplus.com",
        "name": "少年ジャンプ＋",
        "series_id": "14079602755274190581",
    },
    {
        "class": HerosWeb,
        "url": "https://viewer.heros-web.com",
        "name": "コミプレ｜ヒーローズ編集部が運営する無料マンガサイト",
        "series_id": "10834108156672406740",
    },
    {
        "class": TonariNoYoungJump,
        "url": "https://tonarinoyj.jp",
        "name": "となりのヤングジャンプ",
        "series_id": "3269754496306260262",
    },
]


class GigaViewersTest(unittest.TestCase):
    def test_init_website(self):
        for case in TEST_CASES:
            site = case["class"]()

            assert site.url.compose() == case["url"]

    def test_parse_atom(self):
        for case in TEST_CASES:
            site = case["class"]()
            atom = site.parse_root_atom()
            assert atom.feed.title == case["name"]

    def test_parse_series_atom(self):
        for case in TEST_CASES:
            site = case["class"]()
            atom = site.parse_series_atom(case["series_id"])
            assert case["name"] in atom.feed.title


if __name__ == "__main__":
    unittest.main()
