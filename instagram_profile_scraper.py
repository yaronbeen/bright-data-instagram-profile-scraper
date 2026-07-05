"""
Bright Data Instagram Profile Scraper

A Python wrapper for Bright Data's Instagram Profiles scraper API.
Collect profile data (followers, engagement, bio, etc.) by URL.

Dataset ID: gd_l1vikfch901nx3by4
Pricing: $0.0015/record
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union


class InstagramProfileScraper:
    """Client for the Bright Data Instagram Profiles scraper API.

    Collects profile data by URL using Bright Data's dataset infrastructure.
    """

    BASE_URL = "https://api.brightdata.com/datasets/v3/scrape"
    DATASET_ID = "gd_l1vikfch901nx3by4"

    def __init__(self, api_token: Optional[str] = None):
        """Initialize the scraper with a Bright Data API token.

        Args:
            api_token: Bright Data API token. If not provided, reads from
                       the BRIGHT_DATA_API_TOKEN environment variable.

        Raises:
            ValueError: If no API token is provided or found in env.
        """
        self.api_token = api_token or os.getenv("BRIGHT_DATA_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "API token is required. Pass it directly or set the "
                "BRIGHT_DATA_API_TOKEN environment variable."
            )

    def collect_by_url(
        self,
        urls: Union[str, List[str]],
        limit_per_input: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Collect profile data from Instagram profile URLs.

        Args:
            urls: Single URL or list of Instagram profile URLs.
            limit_per_input: Optional limit of records per input.

        Returns:
            List of profile data dictionaries.
        """
        if isinstance(urls, str):
            urls = [urls]

        payload = {
            "input": [{"url": url} for url in urls],
        }
        if limit_per_input is not None:
            payload["limit_per_input"] = limit_per_input

        params = {
            "dataset_id": self.DATASET_ID,
            "include_errors": "true",
        }

        return self._make_request(params, payload)

    def _make_request(
        self, params: Dict[str, str], payload: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Make API request to Bright Data.

        Args:
            params: Query parameters.
            payload: Request body.

        Returns:
            List of result dictionaries.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            params=params,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
