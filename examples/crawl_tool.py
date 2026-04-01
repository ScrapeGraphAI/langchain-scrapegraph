"""Crawl Tool Example - LangChain Tool (v2 API)

Replaces the old SmartCrawler tool. Uses namespaced crawl operations.
"""

import time

from langchain_scrapegraph.tools import CrawlStartTool, CrawlStatusTool

# Initialize tools
start_tool = CrawlStartTool()
status_tool = CrawlStatusTool()

# Start a crawl job
result = start_tool.invoke(
    {
        "url": "https://example.com",
        "depth": 2,
        "max_pages": 5,
        "format": "markdown",
    }
)
print("Crawl started:", result)

# Check status
crawl_id = result.get("id")
if crawl_id:
    time.sleep(5)
    status = status_tool.invoke({"crawl_id": crawl_id})
    print("Crawl status:", status)
