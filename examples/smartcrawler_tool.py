from scrapegraph_py.logger import sgai_logger
import json

from langchain_scrapegraph.tools import SmartCrawlerTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = SmartCrawlerTool()

# Example based on the provided code snippet
url = "https://scrapegraphai.com/"
prompt = "What does the company do? and I need text content from their privacy and terms"

# Use the tool with crawling parameters
result = tool.invoke({
    "url": url,
    "prompt": prompt,
    "cache_website": True,
    "depth": 2,
    "max_pages": 2,
    "same_domain_only": True
})

print(json.dumps(result, indent=2)) 
