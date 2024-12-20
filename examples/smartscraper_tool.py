from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import SmartScraperTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = SmartScraperTool()

# Example website and prompt
website_url = "https://www.example.com"
user_prompt = "Extract the main heading and first paragraph from this webpage"

# Use the tool
result = tool.invoke({"website_url": website_url, "user_prompt": user_prompt})

print(result)
