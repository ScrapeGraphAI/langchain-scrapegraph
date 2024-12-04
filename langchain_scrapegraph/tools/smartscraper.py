from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import SyncClient


class SmartscraperInput(BaseModel):
    user_prompt: str = Field(
        description="Prompt describing what to extract from the website and how to structure the output"
    )
    website_url: str = Field(description="Url of the website to extract data from")


class SmartscraperTool(BaseTool):
    name: str = "Smartscraper"
    description: str = (
        "Useful for when you need to extract structured data from a website, applying also some preprocessing reasoning using LLM"
    )
    args_schema: Type[BaseModel] = SmartscraperInput
    return_direct: bool = True
    client: Optional[SyncClient] = None
    api_key: str
    testing: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = SyncClient(api_key=values["api_key"])
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
        response = self.client.smartscraper(
            website_url=website_url,
            user_prompt=user_prompt,
        )
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
