from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import SearchScraperTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = SearchScraperTool()

# Example prompt
user_prompt = "What are the key features and pricing of ChatGPT Plus?"

# Use the tool
result = tool.invoke({"user_prompt": user_prompt})

print("\nResult:", result)
