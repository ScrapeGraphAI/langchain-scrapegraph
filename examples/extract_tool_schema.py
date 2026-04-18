"""Extract Tool with Schema Example - LangChain Tool (v2 API)"""

from pydantic import BaseModel, Field

from langchain_scrapegraph.tools import ExtractTool


class WebsiteInfo(BaseModel):
    title: str = Field(description="The main title of the page")
    description: str = Field(description="The main description")


# Initialize with output schema
tool = ExtractTool(llm_output_schema=WebsiteInfo)

result = tool.invoke(
    {
        "url": "https://example.com",
        "prompt": "Extract the title and description",
    }
)
print(result)
