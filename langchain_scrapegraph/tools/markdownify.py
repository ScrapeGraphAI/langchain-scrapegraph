from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import MarkdownFormatConfig, ScrapeGraphAI, ScrapeRequest

from langchain_scrapegraph._utils import result_to_dict


class MarkdownifyInput(BaseModel):
    website_url: str = Field(description="Url of the website to convert to Markdown")


class MarkdownifyTool(BaseTool):
    """Tool for converting webpages to Markdown format using ScrapeGraph AI v2 API.

    Under the hood this calls the ``scrape`` endpoint with ``MarkdownFormatConfig``.

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

            result = tool.invoke({"website_url": "https://example.com"})

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({"website_url": "https://example.com"})
    """

    name: str = "Markdownify"
    description: str = (
        "Useful when you need to convert a webpage to Markdown, given a URL as input"
    )
    args_schema: Type[BaseModel] = MarkdownifyInput
    return_direct: bool = True
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = ScrapeGraphAI(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        website_url: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")

        request = ScrapeRequest(url=website_url, formats=[MarkdownFormatConfig()])
        return result_to_dict(self.client.scrape(request))

    async def _arun(
        self,
        website_url: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            website_url,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
