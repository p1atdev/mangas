import os
import unittest

from mangas.websites import ShonenJumpPlus

from dotenv import load_dotenv

load_dotenv(".env.local")

EMAIL = os.environ.get("SHONENJUMPPLUS_EMAIL")
PASSWORD = os.environ.get("SHONENJUMPPLUS_PASSWORD")


class ShonenJumpPlusTest(unittest.TestCase):
    def test_user_login(self):
        assert type(EMAIL) is str
        assert type(PASSWORD) is str

        print("EMAIL:", EMAIL)
        print("PASSWORD:", PASSWORD)

        website = ShonenJumpPlus()

        website.auth = website.login(
            email=EMAIL,
            password=PASSWORD,
        )

        assert website.auth.token is not None
