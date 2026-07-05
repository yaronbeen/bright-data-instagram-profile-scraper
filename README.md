# Bright Data Instagram Profile Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for Bright Data's Instagram Profiles scraper API. Collect detailed Instagram profile data including follower counts, engagement rates, business account status, and more -- without managing proxies, browsers, or CAPTCHAs.

> **All Instagram scrapers:** **Profile Scraper** · [Profile Discovery](https://github.com/yaronbeen/bright-data-instagram-profile-discovery) · [Posts Scraper](https://github.com/yaronbeen/bright-data-instagram-posts-scraper) · [Posts Discovery](https://github.com/yaronbeen/bright-data-instagram-posts-discovery) · [Reels Scraper](https://github.com/yaronbeen/bright-data-instagram-reels-scraper) · [Reels Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-discovery) · [Reels (All) Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-all-discovery) · [Comments Scraper](https://github.com/yaronbeen/bright-data-instagram-comments-scraper)

## Features

- **Collect by URL** -- Retrieve profile data from one or more Instagram profile URLs
- Handles proxy rotation and CAPTCHA solving automatically via Bright Data
- Returns clean, structured JSON ready for analysis
- Simple, Pythonic interface with type hints
- Supports batch requests for multiple profiles at once

## Use Cases

- Track competitor follower growth over time
- Vet influencers before partnerships (engagement rate, business account status)
- Build audience demographics dashboards
- Monitor brand account metrics

## Prerequisites

- Python 3.8 or higher
- A Bright Data API token (create an account at https://brightdata.com)

## Installation

```bash
git clone https://github.com/yaronbeen/bright-data-instagram-profile-scraper.git
cd bright-data-instagram-profile-scraper
pip install -r requirements.txt
```

## Quick Start

### 1. Set your API token

```bash
cp .env.example .env
# Edit .env and add your Bright Data API token
```

Or export it directly:

```bash
export BRIGHT_DATA_API_TOKEN="your_api_token_here"
```

### 2. Create a scraper instance

```python
from instagram_profile_scraper import InstagramProfileScraper

scraper = InstagramProfileScraper()
# Or pass the token directly:
# scraper = InstagramProfileScraper(api_token="your_api_token_here")
```

### 3. Collect profile data

```python
results = scraper.collect_by_url("https://www.instagram.com/leomessi/")
print(results[0]["followers"])
```

## API Reference

### `InstagramProfileScraper(api_token=None)`

Creates a new scraper instance.

| Parameter   | Type          | Required | Description                                                                 |
|-------------|---------------|----------|-----------------------------------------------------------------------------|
| `api_token` | `str \| None` | No       | Bright Data API token. Falls back to `BRIGHT_DATA_API_TOKEN` env variable. |

### `collect_by_url(urls, limit_per_input=None)`

Collect profile data from Instagram profile URLs.

| Parameter         | Type               | Required | Description                          |
|-------------------|--------------------|----------|--------------------------------------|
| `urls`            | `str \| list[str]` | Yes      | Single URL or list of profile URLs.  |
| `limit_per_input` | `int \| None`      | No       | Max records to return per input URL. |

**Returns:** `list[dict]` -- List of profile data dictionaries.

## Example Output

```json
{
  "account": "plantbasedmag",
  "fbid": "17841403842",
  "id": "5821462",
  "followers": 147832,
  "following": 413,
  "posts_count": 2847,
  "is_business_account": true,
  "is_professional_account": true,
  "is_verified": false,
  "avg_engagement": 0.018,
  "external_url": "https://www.plantbasedmag.com",
  "biography": "Plant-powered recipes, tips & lifestyle. New posts daily.",
  "profile_image_link": "https://scontent.cdninstagram.com/v/pbm_pic.jpg",
  "full_name": "Plant Based Magazine",
  "category_name": "Health/Beauty",
  "is_private": false,
  "posts": ["..."]
}
```

> Note: This is a representative example. Actual field values and available fields may vary.

## Configuration

| Environment Variable      | Description                  |
|---------------------------|------------------------------|
| `BRIGHT_DATA_API_TOKEN`   | Your Bright Data API token.  |

You can set the token in a `.env` file (see `.env.example`) or export it in your shell.

## Error Handling

The scraper raises standard exceptions you can catch:

```python
import requests
from instagram_profile_scraper import InstagramProfileScraper

try:
    scraper = InstagramProfileScraper()
    results = scraper.collect_by_url("https://www.instagram.com/leomessi/")
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API")
```

| Exception                          | Cause                                  |
|------------------------------------|----------------------------------------|
| `ValueError`                       | Missing API token.                     |
| `requests.exceptions.HTTPError`    | API returned 4xx/5xx (auth, rate limit, etc.). |
| `requests.exceptions.ConnectionError` | Network connectivity issue.         |
| `requests.exceptions.ReadTimeout`  | Request took longer than 30 seconds.   |

## Rate Limits

- **Sync mode:** Results returned directly in the response. Best for small batches (1-10 inputs).
- **Async mode:** For larger jobs, use the async API. See [Bright Data API docs](https://docs.brightdata.com/datasets/functions/introduction).
- **No hard rate limit** on API calls, but performance varies with batch size.
- **Pricing:** $0.0015 per record ($1.50 per 1,000 records).

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

Instagram blocks profile scraping aggressively. Bright Data handles the hard parts so you can focus on the data:

- **Anti-bot detection handled** - Proxy rotation, CAPTCHA solving, and fingerprint management built in
- **31 structured fields per profile** - No HTML parsing or data extraction logic needed
- **Works on all account types** - Business, creator, and personal accounts alike
- **Fast and reliable** - ~1 second average response time with high success rates
- **$0.0015/record** - Pay only for successful results, no infrastructure to maintain

For full API documentation, see the [Bright Data API Reference](https://docs.brightdata.com/datasets/functions/introduction).

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
