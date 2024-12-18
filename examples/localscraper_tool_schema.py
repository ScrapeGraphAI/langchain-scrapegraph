from typing import List

from pydantic import BaseModel, Field
from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import LocalScraperTool


class WebsiteInfo(BaseModel):
    title: str = Field(description="The main title of the webpage")
    description: str = Field(description="The main description or first paragraph")
    urls: List[str] = Field(description="The URLs inside the webpage")


sgai_logger.set_logging(level="INFO")

# Initialize with Pydantic model class
tool = LocalScraperTool(llm_output_schema=WebsiteInfo)

# Example website and prompt
html_content = """
<html>
    <body>
        <h1>Company Name</h1>
        <p>We are a technology company focused on AI solutions.</p>
        <div class="contact">
            <p>Email: contact@example.com</p>
            <p>Phone: (555) 123-4567</p>
        </div>
    </body>
</html>
"""
user_prompt = "Make a summary of the webpage and extract the email and phone number"

# Use the tool
result = tool.invoke({"website_html": html_content, "user_prompt": user_prompt})

print(result)
