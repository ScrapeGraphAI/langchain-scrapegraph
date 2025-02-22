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

# Example 1: Using website URL
website_url = "https://www.example.com"
user_prompt = "Extract info about the website"

# Use the tool with URL
result_url = tool.invoke({"website_url": website_url, "user_prompt": user_prompt})
print("\nResult from URL:", result_url)

# Example 2: Using HTML content directly
html_content = """
<html>
    <body>
        <h1>Example Domain</h1>
        <p>This domain is for use in illustrative examples.</p>
        <a href="https://www.iana.org/domains/example">More information...</a>
    </body>
</html>
"""

# Use the tool with HTML content
result_html = tool.invoke(
    {
        "website_url": website_url,  # Still required but will be overridden
        "website_html": html_content,
        "user_prompt": user_prompt,
    }
)
print("\nResult from HTML:", result_html)
