from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import MarkdownifyTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = MarkdownifyTool()

# Example website and prompt
website_url = "https://www.example.com"

# Use the tool
result = tool.invoke({"website_url": website_url})

print(result)
