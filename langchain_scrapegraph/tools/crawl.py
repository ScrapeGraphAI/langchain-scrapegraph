from typing import Any, Dict, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import Client


class CrawlStartInput(BaseModel):
    url: str = Field(description="The starting URL for the crawl")
    depth: int = Field(default=2, description="Maximum crawl depth (1-10)")
    max_pages: int = Field(default=10, description="Maximum pages to crawl (1-100)")
    format: str = Field(
        default="markdown", description="Output format: 'markdown' or 'html'"
    )
    include_patterns: Optional[List[str]] = Field(
        default=None, description="URL patterns to include"
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None, description="URL patterns to exclude"
    )


class CrawlIdInput(BaseModel):
    crawl_id: str = Field(description="The crawl job ID")


class CrawlStartTool(BaseTool):
    """Tool for starting a crawl job using ScrapeGraph AI v2 API."""

    name: str = "CrawlStart"
    description: str = (
        "Start a crawl job that will crawl multiple pages from a starting URL. "
        "Returns a job ID that can be used to check status."
    )
    args_schema: Type[BaseModel] = CrawlStartInput
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
        url: str,
        depth: int = 2,
        max_pages: int = 10,
        format: str = "markdown",
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")

        response = self.client.crawl.start(
            url=url,
            depth=depth,
            max_pages=max_pages,
            format=format,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
        return response

    async def _arun(
        self,
        url: str,
        depth: int = 2,
        max_pages: int = 10,
        format: str = "markdown",
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            url=url,
            depth=depth,
            max_pages=max_pages,
            format=format,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class CrawlStatusTool(BaseTool):
    """Tool for getting the status of a crawl job."""

    name: str = "CrawlStatus"
    description: str = "Get the status and results of a crawl job by its ID."
    args_schema: Type[BaseModel] = CrawlIdInput
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
        crawl_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.crawl.status(crawl_id)

    async def _arun(
        self,
        crawl_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            crawl_id=crawl_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class CrawlStopTool(BaseTool):
    """Tool for stopping a running crawl job."""

    name: str = "CrawlStop"
    description: str = "Stop a running crawl job by its ID."
    args_schema: Type[BaseModel] = CrawlIdInput
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
        crawl_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.crawl.stop(crawl_id)

    async def _arun(
        self,
        crawl_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            crawl_id=crawl_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )


class CrawlResumeTool(BaseTool):
    """Tool for resuming a stopped crawl job."""

    name: str = "CrawlResume"
    description: str = "Resume a stopped crawl job by its ID."
    args_schema: Type[BaseModel] = CrawlIdInput
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
        crawl_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.crawl.resume(crawl_id)

    async def _arun(
        self,
        crawl_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        return self._run(
            crawl_id=crawl_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
