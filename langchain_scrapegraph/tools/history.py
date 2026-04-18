from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import HistoryFilter, ScrapeGraphAI

from langchain_scrapegraph._utils import result_to_dict


class HistoryInput(BaseModel):
    service: Optional[str] = Field(
        default=None,
        description="Filter by service name ('scrape', 'extract', 'search', 'monitor', 'crawl')",
    )
    page: int = Field(default=1, description="Page number (starts at 1)")
    limit: int = Field(default=20, description="Number of results per page (1-100)")


class HistoryTool(BaseTool):
    """Tool for retrieving request history from ScrapeGraph AI v2 API."""

    name: str = "History"
    description: str = (
        "Retrieve your ScrapeGraph AI request history with optional service filter and pagination."
    )
    args_schema: Type[BaseModel] = HistoryInput
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
        service: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")

        history_filter = HistoryFilter(page=page, limit=limit, service=service)
        return result_to_dict(self.client.history.list(history_filter))

    async def _arun(
        self,
        service: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            service=service,
            page=page,
            limit=limit,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
