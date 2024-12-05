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

            from langchain_scrapegraph.tools import MarkdownifyTool

            # Will automatically get SGAI_API_KEY from environment
            tool = MarkdownifyTool()

            # Or provide API key directly
            tool = MarkdownifyTool(api_key="your-api-key")

    Use the tool:
        .. code-block:: python

            result = tool.invoke({
                "website_url": "https://example.com"
            })

            print(result)
            # # Example Domain
            #
            # This domain is for use in illustrative examples...

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
        """Validate that api key exists in environment."""
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
        """Use the tool to extract data from a website."""
        if not self.client:
            raise ValueError("Client not initialized")
        response = self.client.markdownify(website_url=website_url)
        return response["result"]

    async def _arun(
        self,
        website_url: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(
            website_url,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
