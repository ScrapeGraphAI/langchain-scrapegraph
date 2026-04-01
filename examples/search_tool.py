"""Search Tool Example - LangChain Tool (v2 API)

Replaces the old SearchScraper tool. Searches the web and extracts structured results.
"""

from langchain_scrapegraph.tools import SearchTool

# Initialize the tool
tool = SearchTool()

# Basic search
result = tool.invoke(
    {
        "query": "What are the key features of ChatGPT Plus?",
    }
)
print(result)

# Search with more results
result = tool.invoke(
    {
        "query": "Latest AI developments 2024",
        "num_results": 10,
    }
)
print(result)
