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
    website_url: str = Field(description="URL of the website to scrape")
    render_heavy_js: bool = Field(
        default=False,
        description="Whether to render heavy JavaScript content (slower but more complete)",
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Optional headers to send with the request"
    )


class ScrapeTool(BaseTool):
    """Tool for getting HTML content from websites using ScrapeGraph AI.

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

            # Will automatically get SGAI_API_KEY from environment
            tool = ScrapeTool()

            # Or provide API key directly
            tool = ScrapeTool(api_key="your-api-key")

    Use the tool:
        .. code-block:: python

            # Basic scraping
            result = tool.invoke({
                "website_url": "https://example.com"
            })

            # With heavy JavaScript rendering
            result = tool.invoke({
                "website_url": "https://example.com",
                "render_heavy_js": True
            })

            # With custom headers
            result = tool.invoke({
                "website_url": "https://example.com",
                "headers": {
                    "User-Agent": "Custom Bot 1.0",
                    "Accept": "text/html"
                }
            })

            print(result)
            # {
            #     "html": "<html>...</html>",
            #     "scrape_request_id": "req_123",
            #     "status": "success",
            #     "error": None
            # }

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "website_url": "https://example.com"
            })
    """

    name: str = "Scrape"
    description: str = (
        "Get HTML content from a website. Useful when you need to retrieve the raw HTML "
        "content of a webpage, with optional heavy JavaScript rendering and custom headers."
    )
    args_schema: Type[BaseModel] = ScrapeInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        website_url: str,
        render_heavy_js: bool = False,
        headers: Optional[Dict[str, str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Use the tool to scrape HTML content from a website."""
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.scrape(
            website_url=website_url,
            render_heavy_js=render_heavy_js,
            headers=headers,
        )

        return response

    async def _arun(
        self,
        website_url: str,
        render_heavy_js: bool = False,
        headers: Optional[Dict[str, str]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Use the tool asynchronously."""
        return self._run(
            website_url=website_url,
            render_heavy_js=render_heavy_js,
            headers=headers,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
