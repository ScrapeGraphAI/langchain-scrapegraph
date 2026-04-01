"""Scrape Tool Example - LangChain Tool (v2 API)"""

from langchain_scrapegraph.tools import ScrapeTool

# Initialize the tool
scrape_tool = ScrapeTool()

# Scrape as markdown (default)
result = scrape_tool.invoke({"url": "https://example.com"})
print("Markdown result:", result)

# Scrape as HTML
result = scrape_tool.invoke({"url": "https://example.com", "format": "html"})
print("HTML result:", result)
