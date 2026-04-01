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


class ExtractInput(BaseModel):
    url: str = Field(description="URL of the webpage to extract data from")
    prompt: str = Field(
        description="Prompt describing what to extract from the webpage and how to structure the output"
    )


class ExtractTool(BaseTool):
    """Tool for extracting structured data from websites using ScrapeGraph AI v2 API.

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

            from langchain_scrapegraph.tools import ExtractTool

            tool = ExtractTool()

            # With output schema:
            from pydantic import BaseModel, Field

            class WebsiteInfo(BaseModel):
                title: str = Field(description="The main title")
                description: str = Field(description="The main description")

            tool_with_schema = ExtractTool(llm_output_schema=WebsiteInfo)

    Use the tool:
        .. code-block:: python

            result = tool.invoke({
                "url": "https://example.com",
                "prompt": "Extract the main heading and first paragraph"
            })

    Async usage:
        .. code-block:: python

            result = await tool.ainvoke({
                "url": "https://example.com",
                "prompt": "Extract the main heading"
            })
    """

    name: str = "Extract"
    description: str = (
        "Extract structured data from a webpage using AI, by providing a URL and an extraction prompt"
    )
    args_schema: Type[BaseModel] = ExtractInput
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
        url: str,
        prompt: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.extract(
            url=url,
            prompt=prompt,
            output_schema=self.llm_output_schema,
        )
        return response

    async def _arun(
        self,
        url: str,
        prompt: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            url,
            prompt,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
