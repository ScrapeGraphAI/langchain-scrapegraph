from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class SmartCrawlerInput(BaseModel):
    prompt: str = Field(
        description="Prompt describing what to extract from the websites and how to structure the output"
    )
    url: str = Field(description="URL of the website to start crawling from")
    cache_website: bool = Field(
        default=True,
        description="Whether to cache the website content for faster subsequent requests",
    )
    depth: int = Field(
        default=2, description="Maximum depth to crawl from the starting URL"
    )
    max_pages: int = Field(default=2, description="Maximum number of pages to crawl")
    same_domain_only: bool = Field(
        default=True,
        description="Whether to only crawl pages from the same domain as the starting URL",
    )


class SmartCrawlerTool(BaseTool):
    """Tool for crawling and extracting structured data from multiple related webpages using ScrapeGraph AI.

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
        llm_output_schema: Optional Pydantic model or dictionary schema to structure the output.
                      If provided, the tool will ensure the output conforms to this schema.

    Instantiate:
        .. code-block:: python

            from langchain_scrapegraph.tools import SmartCrawlerTool

            # Will automatically get SGAI_API_KEY from environment
            tool = SmartCrawlerTool()

            # Or provide API key directly
            tool = SmartCrawlerTool(api_key="your-api-key")

            # Optionally, you can provide an output schema:
            from pydantic import BaseModel, Field

            class CompanyInfo(BaseModel):
                company_description: str = Field(description="What the company does")
                privacy_policy: str = Field(description="Privacy policy content")
                terms_of_service: str = Field(description="Terms of service content")

            tool_with_schema = SmartCrawlerTool(llm_output_schema=CompanyInfo)

    Use the tool:
        .. code-block:: python

            # Basic crawling
            result = tool.invoke({
                "prompt": "What does the company do? Extract privacy and terms content",
                "url": "https://scrapegraphai.com/",
                "depth": 2,
                "max_pages": 5
            })

            # Crawling with custom parameters
            result = tool.invoke({
                "prompt": "Extract product information and pricing",
                "url": "https://example.com/products",
                "cache_website": False,
                "depth": 3,
                "max_pages": 10,
                "same_domain_only": False
            })

            print(result)

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "prompt": "Extract company information",
                "url": "https://example.com"
            })
    """

    name: str = "SmartCrawler"
    description: str = (
        "Useful when you need to extract structured data from multiple related webpages by crawling through a website, applying LLM reasoning across pages, by providing a starting URL and extraction prompt"
    )
    args_schema: Type[BaseModel] = SmartCrawlerInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str
    llm_output_schema: Optional[Type[BaseModel]] = None

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
        prompt: str,
        url: str,
        cache_website: bool = True,
        depth: int = 2,
        max_pages: int = 2,
        same_domain_only: bool = True,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Use the tool to crawl and extract data from multiple webpages."""
        if not self.client:
            raise ValueError("Client not initialized")

        if self.llm_output_schema is None:
            response = self.client.crawl(
                url=url,
                prompt=prompt,
                cache_website=cache_website,
                depth=depth,
                max_pages=max_pages,
                same_domain_only=same_domain_only,
            )
        elif isinstance(self.llm_output_schema, type) and issubclass(
            self.llm_output_schema, BaseModel
        ):
            response = self.client.crawl(
                url=url,
                prompt=prompt,
                cache_website=cache_website,
                depth=depth,
                max_pages=max_pages,
                same_domain_only=same_domain_only,
                output_schema=self.llm_output_schema,
            )
        else:
            raise ValueError("llm_output_schema must be a Pydantic model class")

        return response

    async def _arun(
        self,
        prompt: str,
        url: str,
        cache_website: bool = True,
        depth: int = 2,
        max_pages: int = 2,
        same_domain_only: bool = True,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Use the tool asynchronously."""
        return self._run(
            prompt,
            url,
            cache_website=cache_website,
            depth=depth,
            max_pages=max_pages,
            same_domain_only=same_domain_only,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
