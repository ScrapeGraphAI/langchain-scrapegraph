from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import GetCreditsTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = GetCreditsTool()

# Use the tool
credits = tool.invoke({})

print(credits)
