# Models for agentic scraper endpoint

from typing import Any, Dict, List, Optional, Type
from uuid import UUID

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class AgenticScraperRequest(BaseModel):
    url: str = Field(
        ...,
        example="https://dashboard.scrapegraphai.com/",
        description="The URL to scrape",
    )
    use_session: bool = Field(
        default=True, description="Whether to use session for the scraping"
    )
    steps: List[str] = Field(
        ...,
        example=[
            "Type email@gmail.com in email input box",
            "Type test-password@123 in password inputbox",
            "click on login",
        ],
        description="List of steps to perform on the webpage",
    )
    user_prompt: Optional[str] = Field(
        default=None,
        example="Extract user information and available dashboard sections",
        description="Prompt for AI extraction (only used when ai_extraction=True)",
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        example={
            "user_info": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "dashboard_sections": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            }
        },
        description="Schema for structured data extraction (only used when ai_extraction=True)",
    )
    ai_extraction: bool = Field(
        default=False,
        description="Whether to use AI for data extraction from the scraped content",
    )

    @model_validator(mode="after")
    def validate_url(self) -> "AgenticScraperRequest":
        if not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("Invalid URL - must start with http:// or https://")
        return self

    @model_validator(mode="after")
    def validate_steps(self) -> "AgenticScraperRequest":
        if not self.steps:
            raise ValueError("Steps cannot be empty")
        if any(not step.strip() for step in self.steps):
            raise ValueError("All steps must contain valid instructions")
        return self

    @model_validator(mode="after")
    def validate_ai_extraction(self) -> "AgenticScraperRequest":
        if self.ai_extraction:
            if not self.user_prompt or not self.user_prompt.strip():
                raise ValueError("user_prompt is required when ai_extraction=True")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        # Set exclude_none=True to exclude None values from serialization
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class GetAgenticScraperRequest(BaseModel):
    """Request model for get_agenticscraper endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetAgenticScraperRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self


class AgenticScraperTool(BaseTool):
    """Tool for performing agentic web scraping using ScrapeGraph AI.

    This tool allows you to define a series of steps to perform on a webpage,
    such as filling forms, clicking buttons, and extracting data.

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

            from langchain_scrapegraph.tools import AgenticScraperTool

            # Will automatically get SGAI_API_KEY from environment
            tool = AgenticScraperTool()

            # Or provide API key directly
            tool = AgenticScraperTool(api_key="your-api-key")

    Use the tool:
        .. code-block:: python

            # Basic usage with steps
            result = tool.invoke({
                "url": "https://example.com/login",
                "steps": [
                    "Type 'user@example.com' in email input box",
                    "Type 'password123' in password input box",
                    "Click on login button"
                ]
            })

            # With AI extraction
            result = tool.invoke({
                "url": "https://dashboard.example.com",
                "steps": [
                    "Navigate to user profile section",
                    "Click on settings tab"
                ],
                "ai_extraction": True,
                "user_prompt": "Extract user profile information and available settings",
                "output_schema": {
                    "user_info": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "settings": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            })

    """

    name: str = "agentic_scraper"
    description: str = (
        "Perform agentic web scraping by executing a series of steps on a webpage. "
        "Supports form filling, button clicking, navigation, and AI-powered data extraction."
    )
    args_schema: Type[BaseModel] = AgenticScraperRequest
    return_direct: bool = False

    api_key: Optional[str] = Field(default=None, description="ScrapeGraph AI API key")
    client: Optional[Client] = Field(
        default=None, description="ScrapeGraph client instance"
    )
    llm_output_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Optional Pydantic model to structure the output"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = get_from_dict_or_env(kwargs, "api_key", "SGAI_API_KEY")
        if not self.client:
            self.client = Client(api_key=self.api_key)

    def _run(
        self,
        url: str,
        steps: List[str],
        use_session: bool = True,
        user_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        ai_extraction: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Run the agentic scraper tool."""
        try:
            # Prepare the request payload
            payload = {
                "url": url,
                "use_session": use_session,
                "steps": steps,
                "ai_extraction": ai_extraction,
            }

            if ai_extraction and user_prompt:
                payload["user_prompt"] = user_prompt
                if output_schema:
                    payload["output_schema"] = output_schema

            # Call the ScrapeGraph API
            response = self.client.agentic_scraper(**payload)

            return response

        except Exception as e:
            if run_manager:
                run_manager.on_tool_error(e, tool_name=self.name)
            raise e

    async def _arun(
        self,
        url: str,
        steps: List[str],
        use_session: bool = True,
        user_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        ai_extraction: bool = False,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Run the agentic scraper tool asynchronously."""
        # For now, just call the sync version
        # In a real implementation, you might want to use async HTTP client
        return self._run(
            url=url,
            steps=steps,
            use_session=use_session,
            user_prompt=user_prompt,
            output_schema=output_schema,
            ai_extraction=ai_extraction,
            run_manager=run_manager,
        )
