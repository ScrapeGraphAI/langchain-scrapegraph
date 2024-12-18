from typing import List

from pydantic import BaseModel, Field
from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import SmartScraperTool


class WebsiteInfo(BaseModel):
    title: str = Field(description="The main title of the webpage")
    description: str = Field(description="The main description or first paragraph")
    urls: List[str] = Field(description="The URLs inside the webpage")


sgai_logger.set_logging(level="INFO")

# Initialize with Pydantic model class
tool = SmartScraperTool(llm_output_schema=WebsiteInfo)

# Example website and prompt
website_url = "https://www.example.com"
user_prompt = "Extract info about the website"

# Use the tool - output will conform to WebsiteInfo schema
result = tool.invoke({"website_url": website_url, "user_prompt": user_prompt})
print(result)
