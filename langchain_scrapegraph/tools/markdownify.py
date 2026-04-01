from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class MarkdownifyInput(BaseModel):
    website_url: str = Field(description="Url of the website to convert to Markdown")


class MarkdownifyTool(BaseTool):
    """Tool for converting webpages to Markdown format using ScrapeGraph AI.

    In v2, this uses the scrape endpoint with format='markdown'.

    Setup:
        Install ``langchain-scrapegraph`` python package:

        .. code-block:: bash

            pip install langchain-scrapegraph

        Get your API key from ScrapeGraph AI (https://scrapegraphai.com)
        and set it as an environment variable:

        .. code-block:: bash

            export SGAI_API_KEY="your-api-key"

    Instantiate:
        .. code-block:: python

            from langchain_scrapegraph.tools import MarkdownifyTool

            tool = MarkdownifyTool()

    Use the tool:
        .. code-block:: python

            result = tool.invoke({
                "website_url": "https://example.com"
            })

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "website_url": "https://example.com"
            })
    """

    name: str = "Markdownify"
    description: str = (
        "Useful when you need to convert a webpage to Markdown, given a URL as input"
    )
    args_schema: Type[BaseModel] = MarkdownifyInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        website_url: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        response = self.client.scrape(url=website_url, format="markdown")
        return response

    async def _arun(
        self,
        website_url: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            website_url,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
