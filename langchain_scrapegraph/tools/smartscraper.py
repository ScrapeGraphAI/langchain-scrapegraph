from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class SmartScraperInput(BaseModel):
    user_prompt: str = Field(
        description="Prompt describing what to extract from the webpage and how to structure the output"
    )
    website_url: str = Field(description="Url of the webpage to extract data from")


class SmartScraperTool(BaseTool):
    """Tool for extracting structured data from websites using ScrapeGraph AI.

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

            from langchain_scrapegraph.tools import SmartScraperTool

            # Will automatically get SGAI_API_KEY from environment
            tool = SmartScraperTool()

            # Or provide API key directly
            tool = SmartScraperTool(api_key="your-api-key")

            # Optionally, you can provide an output schema:
            from pydantic import BaseModel, Field

            class WebsiteInfo(BaseModel):
                title: str = Field(description="The main title")
                description: str = Field(description="The main description")

            tool_with_schema = SmartScraperTool(llm_output_schema=WebsiteInfo)

    Use the tool:
        .. code-block:: python

            result = tool.invoke({
                "user_prompt": "Extract the main heading and first paragraph",
                "website_url": "https://example.com"
            })

            print(result)
            # Without schema:
            # {
            #     "main_heading": "Example Domain",
            #     "first_paragraph": "This domain is for use in illustrative examples..."
            # }
            #
            # With WebsiteInfo schema:
            # {
            #     "title": "Example Domain",
            #     "description": "This domain is for use in illustrative examples..."
            # }

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "user_prompt": "Extract the main heading",
                "website_url": "https://example.com"
            })
    """

    name: str = "SmartScraper"
    description: str = (
        "Useful when you need to extract structured data from a webpage, applying also some reasoning using LLM, by providing a webpage URL and an extraction prompt"
    )
    args_schema: Type[BaseModel] = SmartScraperInput
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
        user_prompt: str,
        website_url: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Use the tool to extract data from a website."""
        if not self.client:
            raise ValueError("Client not initialized")

        if self.llm_output_schema is None:
            response = self.client.smartscraper(
                website_url=website_url,
                user_prompt=user_prompt,
            )
        elif isinstance(self.llm_output_schema, type) and issubclass(
            self.llm_output_schema, BaseModel
        ):
            response = self.client.smartscraper(
                website_url=website_url,
                user_prompt=user_prompt,
                output_schema=self.llm_output_schema,
            )
        else:
            raise ValueError("llm_output_schema must be a Pydantic model class")

        return response["result"]

    async def _arun(
        self,
        user_prompt: str,
        website_url: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return self._run(
            user_prompt,
            website_url,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
