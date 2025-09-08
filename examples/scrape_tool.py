#!/usr/bin/env python3
"""Scrape Tool Example - LangChain Tool"""

import time
from pathlib import Path

from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import ScrapeTool

sgai_logger.set_logging(level="INFO")


def save_html_content(
    html_content: str, filename: str, output_dir: str = "scrape_output"
):
    """
    Save HTML content to a file.

    Args:
        html_content: The HTML content to save
        filename: The name of the file (without extension)
        output_dir: The directory to save the file in
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Save HTML file
    html_file = output_path / f"{filename}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML content saved to: {html_file}")
    return html_file


def analyze_html_content(html_content: str) -> dict:
    """
    Analyze HTML content and provide basic statistics.

    Args:
        html_content: The HTML content to analyze

    Returns:
        dict: Basic statistics about the HTML content
    """
    stats = {
        "total_length": len(html_content),
        "lines": len(html_content.splitlines()),
        "has_doctype": html_content.strip().startswith("<!DOCTYPE"),
        "has_html_tag": "<html" in html_content.lower(),
        "has_head_tag": "<head" in html_content.lower(),
        "has_body_tag": "<body" in html_content.lower(),
        "script_tags": html_content.lower().count("<script"),
        "style_tags": html_content.lower().count("<style"),
        "div_tags": html_content.lower().count("<div"),
        "p_tags": html_content.lower().count("<p"),
        "img_tags": html_content.lower().count("<img"),
        "link_tags": html_content.lower().count("<link"),
    }

    return stats


def main():
    """
    Main function demonstrating Scrape Tool usage.
    """
    # Example websites to test
    test_websites = [
        {
            "url": "https://example.com",
            "name": "example",
            "render_heavy_js": False,
            "description": "Simple static website",
        },
        {
            "url": "https://httpbin.org/html",
            "name": "httpbin_html",
            "render_heavy_js": False,
            "description": "HTTP testing service",
        },
    ]

    print("Scrape Tool Example - LangChain Tool")
    print("=" * 50)

    # Initialize the tool
    try:
        scrape_tool = ScrapeTool()
        print("✅ Scrape tool initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize scrape tool: {str(e)}")
        print("Make sure you have SGAI_API_KEY in your environment")
        return

    for website in test_websites:
        print(f"\nTesting: {website['description']}")
        print("-" * 40)

        try:
            # Get HTML content using the tool
            start_time = time.time()

            js_mode = (
                "with heavy JS rendering"
                if website["render_heavy_js"]
                else "without JS rendering"
            )
            print(f"Getting HTML content from: {website['url']}")
            print(f"Mode: {js_mode}")

            result = scrape_tool.invoke(
                {
                    "website_url": website["url"],
                    "render_heavy_js": website["render_heavy_js"],
                }
            )

            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time:.2f} seconds")

            # Display response metadata
            print(f"Request ID: {result.get('scrape_request_id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Error: {result.get('error', 'None')}")

            # Analyze HTML content
            html_content = result.get("html", "")
            if html_content:
                stats = analyze_html_content(html_content)
                print("\nHTML Content Analysis:")
                print(f"  Total length: {stats['total_length']:,} characters")
                print(f"  Lines: {stats['lines']:,}")
                print(f"  Has DOCTYPE: {stats['has_doctype']}")
                print(f"  Has HTML tag: {stats['has_html_tag']}")
                print(f"  Has Head tag: {stats['has_head_tag']}")
                print(f"  Has Body tag: {stats['has_body_tag']}")
                print(f"  Script tags: {stats['script_tags']}")
                print(f"  Style tags: {stats['style_tags']}")
                print(f"  Div tags: {stats['div_tags']}")
                print(f"  Paragraph tags: {stats['p_tags']}")
                print(f"  Image tags: {stats['img_tags']}")
                print(f"  Link tags: {stats['link_tags']}")

                # Save HTML content
                filename = f"{website['name']}_{'js' if website['render_heavy_js'] else 'nojs'}"
                save_html_content(html_content, filename)

                # Show first 500 characters as preview
                preview = html_content[:500].replace("\n", " ").strip()
                print("\nHTML Preview (first 500 chars):")
                print(f"  {preview}...")
            else:
                print("No HTML content received")

        except Exception as e:
            print(f"Error processing {website['url']}: {str(e)}")

        print("\n" + "=" * 50)

    # Test with custom headers
    print("\nTesting with custom headers...")
    print("-" * 40)

    try:
        custom_headers = {
            "User-Agent": "LangChain-ScrapeTool/1.0",
            "Accept": "text/html,application/xhtml+xml",
        }

        result = scrape_tool.invoke(
            {"website_url": "https://httpbin.org/headers", "headers": custom_headers}
        )

        print("Custom headers test:")
        print(f"Status: {result.get('status', 'N/A')}")

        html_content = result.get("html", "")
        if html_content:
            print(f"Content length: {len(html_content)} characters")
            # Look for our custom User-Agent in the response
            if "LangChain-ScrapeTool" in html_content:
                print("✅ Custom User-Agent header was sent successfully")
            else:
                print("⚠️ Custom User-Agent not found in response")

    except Exception as e:
        print(f"Error testing custom headers: {str(e)}")

    print("\n🎉 Scrape tool example completed successfully!")


if __name__ == "__main__":
    main()
