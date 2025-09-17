#!/usr/bin/env python3
"""
SmartScraper Heavy JavaScript Example

This example demonstrates how to use SmartScraper with render_heavy_js enabled
for scraping JavaScript-heavy websites that require full browser rendering.

Features demonstrated:
- SmartScraper with heavy JavaScript rendering
- Basic error handling
- Environment variable configuration
- Simple API usage pattern

Requirements:
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

import os

from dotenv import load_dotenv
from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

# Load environment variables from .env file
load_dotenv()

sgai_logger.set_logging(level="INFO")


def main():
    """Run a SmartScraper example with heavy JavaScript rendering."""
    print("🌐 SmartScraper Heavy JavaScript Example")
    print("=" * 50)

    # Initialize the client with API key from environment variable
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        print("Please either:")
        print("  1. Set environment variable: export SGAI_API_KEY='your-api-key-here'")
        print("  2. Create a .env file with: SGAI_API_KEY=your-api-key-here")
        return False

    client = Client(api_key=api_key)

    try:
        # Configuration
        website_url = "https://example.com"  # Replace with your target URL
        user_prompt = "Find the CEO of company X and their contact details"

        print(f"🔗 Target URL: {website_url}")
        print(f"📝 Query: {user_prompt}")
        print("🔧 Mode: Heavy JavaScript rendering enabled")

        # SmartScraper request with render_heavy_js enabled
        response = client.smartscraper(
            website_url=website_url,
            user_prompt=user_prompt,
            render_heavy_js=True,  # Enable heavy JavaScript rendering
        )

        print("\n✅ SmartScraper completed successfully!")
        print(f"📄 Request ID: {response.get('request_id', 'N/A')}")

        # Display the results
        if "result" in response:
            print("\n📝 Extracted Information:")
            print(response["result"])

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

    finally:
        # Close the client
        client.close()


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
