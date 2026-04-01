from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class HistoryInput(BaseModel):
    endpoint: Optional[str] = Field(
        default=None,
        description="Filter by endpoint name (e.g. 'scrape', 'extract', 'search')",
    )
    status: Optional[str] = Field(default=None, description="Filter by request status")
    limit: Optional[int] = Field(
        default=None, description="Maximum number of results (1-100)"
    )
    offset: Optional[int] = Field(default=None, description="Number of results to skip")


class HistoryTool(BaseTool):
    """Tool for retrieving request history from ScrapeGraph AI v2 API."""

    name: str = "History"
    description: str = (
        "Retrieve your ScrapeGraph AI request history with optional filters."
    )
    args_schema: Type[BaseModel] = HistoryInput
    return_direct: bool = True
    client: Optional[Client] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = Client(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        endpoint: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")

        return self.client.history(
            endpoint=endpoint,
            status=status,
            limit=limit,
            offset=offset,
        )

    async def _arun(
        self,
        endpoint: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            endpoint=endpoint,
            status=status,
            limit=limit,
            offset=offset,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
