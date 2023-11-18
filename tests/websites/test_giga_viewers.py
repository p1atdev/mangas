import unittest

from mangas.websites import ShonenJumpPlus, HerosWeb, TonariNoYoungJump


TEST_CASES = [
    {
        "class": ShonenJumpPlus,
        "url": "https://shonenjumpplus.com",
        "name": "少年ジャンプ＋",
    },
    {
        "class": HerosWeb,
        "url": "https://viewer.heros-web.com",
        "name": "コミプレ｜ヒーローズ編集部が運営する無料マンガサイト",
    },
    {
        "class": TonariNoYoungJump,
        "url": "https://tonarinoyj.jp",
        "name": "となりのヤングジャンプ",
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
            atom = site.parse_atom()
            assert atom.feed.title == case["name"]


if __name__ == "__main__":
    unittest.main()
