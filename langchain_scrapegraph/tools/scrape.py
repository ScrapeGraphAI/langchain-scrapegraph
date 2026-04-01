from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class ScrapeInput(BaseModel):
    url: str = Field(description="URL of the website to scrape")
    format: str = Field(
        default="markdown",
        description="Output format: 'markdown', 'html', 'screenshot', or 'branding'",
    )


class ScrapeTool(BaseTool):
    """Tool for scraping web pages using ScrapeGraph AI v2 API.

    Returns content in the specified format (markdown, html, screenshot, or branding).

    Setup:
        Install ``langchain-scrapegraph`` python package:

        .. code-block:: bash

            pip install langchain-scrapegraph

        Get your API key from ScrapeGraph AI (https://scrapegraphai.com)
        and set it as an environment variable:

        .. code-block:: bash

            export SGAI_API_KEY="your-api-key"

    Key init args:
        api_key: Your ScrapeGraph AI API key. If not provided, will look for SGAI_API_KEY env var.
        client: Optional pre-configured ScrapeGraph client instance.

    Instantiate:
        .. code-block:: python

            from langchain_scrapegraph.tools import ScrapeTool

            tool = ScrapeTool()

    Use the tool:
        .. code-block:: python

            # Get markdown content
            result = tool.invoke({
                "url": "https://example.com"
            })

            # Get HTML content
            result = tool.invoke({
                "url": "https://example.com",
                "format": "html"
            })

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "url": "https://example.com"
            })
    """

    name: str = "Scrape"
    description: str = (
        "Scrape a web page and return its content in the specified format "
        "(markdown, html, screenshot, or branding)."
    )
    args_schema: Type[BaseModel] = ScrapeInput
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
        url: str,
        format: str = "markdown",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.scrape(url=url, format=format)
        return response

    async def _arun(
        self,
        url: str,
        format: str = "markdown",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            url=url,
            format=format,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
