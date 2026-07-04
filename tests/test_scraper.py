"""Comprehensive tests for InstagramProfileScraper."""

import os
import unittest
from unittest.mock import patch, MagicMock

import requests

from instagram_profile_scraper import InstagramProfileScraper


SAMPLE_PROFILE = {
    "account": "cats_of_world_",
    "fbid": "12345678",
    "id": "12345678",
    "followers": 500000,
    "posts_count": 1200,
    "is_business_account": True,
    "is_professional_account": True,
    "is_verified": False,
    "avg_engagement": 0.035,
    "external_url": "https://example.com",
    "biography": "Best cat photos from around the world",
    "profile_pic_url": "https://example.com/pic.jpg",
    "full_name": "Cats of the World",
    "category": "Pets",
}


class TestInstagramProfileScraperInit(unittest.TestCase):
    """Tests for __init__ / authentication."""

    def test_init_with_token_argument(self):
        scraper = InstagramProfileScraper(api_token="test_token_123")
        self.assertEqual(scraper.api_token, "test_token_123")

    @patch.dict(os.environ, {"BRIGHT_DATA_API_TOKEN": "env_token_456"})
    def test_init_with_env_variable(self):
        scraper = InstagramProfileScraper()
        self.assertEqual(scraper.api_token, "env_token_456")

    @patch.dict(os.environ, {"BRIGHT_DATA_API_TOKEN": "env_token"})
    def test_init_argument_takes_precedence_over_env(self):
        scraper = InstagramProfileScraper(api_token="arg_token")
        self.assertEqual(scraper.api_token, "arg_token")

    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_token_raises(self):
        with self.assertRaises(ValueError) as ctx:
            InstagramProfileScraper()
        self.assertIn("API token is required", str(ctx.exception))


class TestCollectByUrl(unittest.TestCase):
    """Tests for collect_by_url."""

    def setUp(self):
        self.scraper = InstagramProfileScraper(api_token="test_token")

    @patch("instagram_profile_scraper.requests.post")
    def test_single_url_string(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = self.scraper.collect_by_url("https://www.instagram.com/cats_of_world_/")

        self.assertEqual(result, [SAMPLE_PROFILE])
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(
            payload["input"],
            [{"url": "https://www.instagram.com/cats_of_world_/"}],
        )
        self.assertNotIn("limit_per_input", payload)

    @patch("instagram_profile_scraper.requests.post")
    def test_multiple_urls_list(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE, SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        urls = [
            "https://www.instagram.com/cats_of_world_/",
            "https://www.instagram.com/natgeo/",
        ]
        result = self.scraper.collect_by_url(urls)

        self.assertEqual(len(result), 2)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(len(payload["input"]), 2)
        self.assertEqual(payload["input"][0], {"url": urls[0]})
        self.assertEqual(payload["input"][1], {"url": urls[1]})

    @patch("instagram_profile_scraper.requests.post")
    def test_collect_url_params(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/")

        call_kwargs = mock_post.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params")
        self.assertEqual(params["dataset_id"], "gd_l1vikfch901nx3by4")
        self.assertEqual(params["include_errors"], "true")
        # collect_by_url should NOT have type or discover_by
        self.assertNotIn("type", params)
        self.assertNotIn("discover_by", params)

    @patch("instagram_profile_scraper.requests.post")
    def test_collect_url_headers(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/")

        call_kwargs = mock_post.call_args
        headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers")
        self.assertEqual(headers["Authorization"], "Bearer test_token")
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("instagram_profile_scraper.requests.post")
    def test_collect_with_limit_per_input(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/", limit_per_input=5)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(payload["limit_per_input"], 5)


class TestDiscoverByUsername(unittest.TestCase):
    """Tests for discover_by_username."""

    def setUp(self):
        self.scraper = InstagramProfileScraper(api_token="test_token")

    @patch("instagram_profile_scraper.requests.post")
    def test_single_username_string(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = self.scraper.discover_by_username("zoobarcelona")

        self.assertEqual(result, [SAMPLE_PROFILE])
        mock_post.assert_called_once()

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(payload["input"], [{"user_name": "zoobarcelona"}])
        self.assertNotIn("limit_per_input", payload)

    @patch("instagram_profile_scraper.requests.post")
    def test_multiple_usernames_list(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE, SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        usernames = ["zoobarcelona", "natgeo"]
        result = self.scraper.discover_by_username(usernames)

        self.assertEqual(len(result), 2)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(len(payload["input"]), 2)
        self.assertEqual(payload["input"][0], {"user_name": "zoobarcelona"})
        self.assertEqual(payload["input"][1], {"user_name": "natgeo"})

    @patch("instagram_profile_scraper.requests.post")
    def test_discover_url_params(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.discover_by_username("test_user")

        call_kwargs = mock_post.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params")
        self.assertEqual(params["dataset_id"], "gd_l1vikfch901nx3by4")
        self.assertEqual(params["type"], "discover_new")
        self.assertEqual(params["discover_by"], "user_name")
        self.assertEqual(params["include_errors"], "true")

    @patch("instagram_profile_scraper.requests.post")
    def test_discover_with_limit_per_input(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.discover_by_username("test_user", limit_per_input=10)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(payload["limit_per_input"], 10)


class TestRequestUrl(unittest.TestCase):
    """Tests that the correct base URL is used."""

    def setUp(self):
        self.scraper = InstagramProfileScraper(api_token="test_token")

    @patch("instagram_profile_scraper.requests.post")
    def test_base_url(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/")

        call_args = mock_post.call_args
        url = call_args.args[0] if call_args.args else call_args[0][0]
        self.assertEqual(url, "https://api.brightdata.com/datasets/v3/scrape")


class TestErrorHandling(unittest.TestCase):
    """Tests for HTTP error handling."""

    def setUp(self):
        self.scraper = InstagramProfileScraper(api_token="test_token")

    @patch("instagram_profile_scraper.requests.post")
    def test_401_unauthorized(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=401)
        )
        mock_post.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.collect_by_url("https://www.instagram.com/test/")

    @patch("instagram_profile_scraper.requests.post")
    def test_500_server_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=500)
        )
        mock_post.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.discover_by_username("test_user")

    @patch("instagram_profile_scraper.requests.post")
    def test_connection_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.scraper.collect_by_url("https://www.instagram.com/test/")

    @patch("instagram_profile_scraper.requests.post")
    def test_timeout_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ReadTimeout("Read timed out")

        with self.assertRaises(requests.exceptions.ReadTimeout):
            self.scraper.collect_by_url("https://www.instagram.com/test/")


class TestRequestTimeout(unittest.TestCase):
    """Tests that requests include a timeout."""

    def setUp(self):
        self.scraper = InstagramProfileScraper(api_token="test_token")

    @patch("instagram_profile_scraper.requests.post")
    def test_request_includes_timeout(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/")

        call_kwargs = mock_post.call_args
        timeout = call_kwargs.kwargs.get("timeout") or call_kwargs[1].get("timeout")
        self.assertIsNotNone(timeout)
        self.assertGreater(timeout, 0)


class TestPayloadLimitPerInput(unittest.TestCase):
    """Tests that limit_per_input is only included when set."""

    def setUp(self):
        self.scraper = InstagramProfileScraper(api_token="test_token")

    @patch("instagram_profile_scraper.requests.post")
    def test_limit_excluded_when_none(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertNotIn("limit_per_input", payload)

    @patch("instagram_profile_scraper.requests.post")
    def test_limit_included_when_set(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.collect_by_url("https://www.instagram.com/test/", limit_per_input=3)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(payload["limit_per_input"], 3)

    @patch("instagram_profile_scraper.requests.post")
    def test_discover_limit_excluded_when_none(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.discover_by_username("test_user")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertNotIn("limit_per_input", payload)

    @patch("instagram_profile_scraper.requests.post")
    def test_discover_limit_included_when_set(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = [SAMPLE_PROFILE]
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.scraper.discover_by_username("test_user", limit_per_input=7)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(payload["limit_per_input"], 7)


if __name__ == "__main__":
    unittest.main()
