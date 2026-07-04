"""Example: Collect Instagram profile data by URL."""

import json
import sys
import os

from dotenv import load_dotenv

# Allow running directly from the examples/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from instagram_profile_scraper import InstagramProfileScraper

load_dotenv()


def main():
    scraper = InstagramProfileScraper()

    # Collect data for multiple Instagram profiles
    urls = [
        "https://www.instagram.com/cats_of_world_/",
        "https://www.instagram.com/natgeo/",
    ]

    print(f"Collecting profile data for {len(urls)} URLs...")
    results = scraper.collect_by_url(urls)

    for profile in results:
        print("\n" + "=" * 60)
        print(f"Account:    {profile.get('account', 'N/A')}")
        print(f"Full Name:  {profile.get('full_name', 'N/A')}")
        print(f"Followers:  {profile.get('followers', 'N/A')}")
        print(f"Posts:      {profile.get('posts_count', 'N/A')}")
        print(f"Verified:   {profile.get('is_verified', 'N/A')}")
        print(f"Business:   {profile.get('is_business_account', 'N/A')}")
        print(f"Bio:        {profile.get('biography', 'N/A')}")

    # Print full JSON for the first result
    if results:
        print("\n\nFull JSON for first profile:")
        print(json.dumps(results[0], indent=2, default=str))


if __name__ == "__main__":
    main()
