from typing import Any, Dict, Optional, Type, TypeVar

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client

T = TypeVar("T", bound=BaseModel)


class SearchScraperInput(BaseModel):
    user_prompt: str = Field(
        description="Prompt describing what information to search for and extract from the web"
    )
    extraction_mode: bool = Field(
        default=True,
        description="If True, use AI extraction mode (10 credits/page). If False, use markdown mode (2 credits/page).",
    )


class SearchScraperTool(BaseTool):
    """Tool for searching and extracting structured data from the web using ScrapeGraph AI.

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

            from langchain_scrapegraph.tools import SearchScraperTool

            # Will automatically get SGAI_API_KEY from environment
            tool = SearchScraperTool()

            # Or provide API key directly
            tool = SearchScraperTool(api_key="your-api-key")

            # Optionally, you can provide an output schema:
            from pydantic import BaseModel, Field
            from typing import List

            class ProductInfo(BaseModel):
                name: str = Field(description="Product name")
                features: List[str] = Field(description="List of product features")
                pricing: Dict[str, Any] = Field(description="Pricing information")

            tool_with_schema = SearchScraperTool(llm_output_schema=ProductInfo)

    Use the tool:
        .. code-block:: python

            result = tool.invoke({
                "user_prompt": "What are the key features and pricing of ChatGPT Plus?"
            })

            print(result)
            # {
            #     "product": {
            #         "name": "ChatGPT Plus",
            #         "description": "Premium version of ChatGPT...",
            #         ...
            #     },
            #     "features": [...],
            #     "pricing": {...},
            #     "reference_urls": [
            #         "https://openai.com/chatgpt",
            #         ...
            #     ]
            # }

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "user_prompt": "What are the key features of Product X?"
            })
    """

    name: str = "SearchScraper"
    description: str = (
        "Useful when you need to search and extract structured information from the web about a specific topic or query"
    )
    args_schema: Type[BaseModel] = SearchScraperInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str
    llm_output_schema: Optional[Type[BaseModel]] = None

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls: Type[T], values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        user_prompt: str,
        extraction_mode: bool = True,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Use the tool to search and extract data from the web.

        Args:
            user_prompt: What information to search for and extract
            extraction_mode: If True, use AI extraction (10 credits/page). If False, use markdown mode (2 credits/page).
            run_manager: Optional callback manager

        Returns:
            dict: In extraction mode, returns structured data. In markdown mode, returns markdown content.
        """
        if not self.client:
            raise ValueError("Client not initialized")

        # In markdown mode, we ignore the output schema since we're returning raw markdown
        if not extraction_mode:
            response = self.client.searchscraper(
                user_prompt=user_prompt,
                extraction_mode=False,
            )
            return {
                "markdown_content": response.get("markdown_content", ""),
                "reference_urls": response.get("reference_urls", []),
            }

        # In extraction mode, we can use the output schema if provided
        if self.llm_output_schema is None:
            response = self.client.searchscraper(
                user_prompt=user_prompt,
                extraction_mode=True,
            )
        elif isinstance(self.llm_output_schema, type) and issubclass(
            self.llm_output_schema, BaseModel
        ):
            response = self.client.searchscraper(
                user_prompt=user_prompt,
                extraction_mode=True,
                output_schema=self.llm_output_schema,
            )
        else:
            raise ValueError("llm_output_schema must be a Pydantic model class")

        return response["result"]

    async def _arun(
        self,
        user_prompt: str,
        extraction_mode: bool = True,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Use the tool asynchronously."""
        return self._run(
            user_prompt,
            extraction_mode=extraction_mode,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
