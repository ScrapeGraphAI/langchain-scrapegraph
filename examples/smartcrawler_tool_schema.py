from pydantic import BaseModel, Field
from scrapegraph_py.logger import sgai_logger
import json

from langchain_scrapegraph.tools import SmartCrawlerTool

sgai_logger.set_logging(level="INFO")

# Define the output schema
class CompanyInfo(BaseModel):
    company_description: str = Field(description="What the company does")
    privacy_policy: str = Field(description="Privacy policy content")
    terms_of_service: str = Field(description="Terms of service content")

# Initialize the tool with the schema
tool = SmartCrawlerTool(llm_output_schema=CompanyInfo)

# Example crawling with structured output
url = "https://scrapegraphai.com/"
prompt = "What does the company do? and I need text content from their privacy and terms"

# Use the tool with crawling parameters and structured output
result = tool.invoke({
    "url": url,
    "prompt": prompt,
    "cache_website": True,
    "depth": 2,
    "max_pages": 2,
    "same_domain_only": True
})

print(json.dumps(result, indent=2))

# The output will be structured according to the CompanyInfo schema:
# {
#   "company_description": "...",
#   "privacy_policy": "...",
#   "terms_of_service": "..."
# } 