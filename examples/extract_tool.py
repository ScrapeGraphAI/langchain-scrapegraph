"""Extract Tool Example - LangChain Tool (v2 API)

Replaces the old SmartScraper tool. Extracts structured data from webpages using AI.
"""

from langchain_scrapegraph.tools import ExtractTool

# Initialize the tool
tool = ExtractTool()

# Basic extraction
result = tool.invoke(
    {
        "url": "https://example.com",
        "prompt": "Extract the main heading and first paragraph",
    }
)
print(result)
