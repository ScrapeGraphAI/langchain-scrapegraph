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


class SearchInput(BaseModel):
    query: str = Field(
        description="The search query describing what information to find on the web"
    )
    num_results: int = Field(
        default=5,
        description="Number of search results to return (3-20)",
    )


class SearchTool(BaseTool):
    """Tool for searching the web and extracting structured data using ScrapeGraph AI v2 API.

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
        llm_output_schema: Optional Pydantic model class to structure the output.

    Instantiate:
        .. code-block:: python

            from langchain_scrapegraph.tools import SearchTool

            tool = SearchTool()

    Use the tool:
        .. code-block:: python

            result = tool.invoke({
                "query": "What are the key features of ChatGPT Plus?"
            })

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "query": "What are the key features of Product X?"
            })
    """

    name: str = "Search"
    description: str = (
        "Search the web and extract structured information about a specific topic or query"
    )
    args_schema: Type[BaseModel] = SearchInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str
    llm_output_schema: Optional[Type[BaseModel]] = None

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls: Type[T], values: Dict[str, Any]) -> Dict[str, Any]:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        query: str,
        num_results: int = 5,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.search(
            query=query,
            num_results=num_results,
            output_schema=self.llm_output_schema,
        )
        return response

    async def _arun(
        self,
        query: str,
        num_results: int = 5,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            query,
            num_results=num_results,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
