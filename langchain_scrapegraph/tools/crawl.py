from typing import Any, Dict, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import CrawlRequest, ScrapeGraphAI

from langchain_scrapegraph._utils import format_config, result_to_dict


class CrawlStartInput(BaseModel):
    url: str = Field(description="The starting URL for the crawl")
    max_depth: int = Field(default=2, description="Maximum crawl depth")
    max_pages: int = Field(default=50, description="Maximum pages to crawl (1-1000)")
    format: str = Field(
        default="markdown",
        description="Output format: 'markdown', 'html', 'screenshot', 'branding', 'links', 'images', or 'summary'",
    )
    allow_external: bool = Field(
        default=False, description="Whether to follow links to other domains"
    )
    include_patterns: Optional[List[str]] = Field(
        default=None, description="URL patterns to include"
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None, description="URL patterns to exclude"
    )


class CrawlIdInput(BaseModel):
    crawl_id: str = Field(description="The crawl job ID")


def _make_client(values: Dict) -> Dict:
    values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
    values["client"] = ScrapeGraphAI(api_key=values["api_key"])
    return values


class CrawlStartTool(BaseTool):
    """Tool for starting a crawl job using ScrapeGraph AI v2 API."""

    name: str = "CrawlStart"
    description: str = (
        "Start a crawl job that will crawl multiple pages from a starting URL. "
        "Returns a job ID that can be used to check status."
    )
    args_schema: Type[BaseModel] = CrawlStartInput
    return_direct: bool = True
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        url: str,
        max_depth: int = 2,
        max_pages: int = 50,
        format: str = "markdown",
        allow_external: bool = False,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")

        request = CrawlRequest(
            url=url,
            max_depth=max_depth,
            max_pages=max_pages,
            formats=[format_config(format)],
            allow_external=allow_external,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
        return result_to_dict(self.client.crawl.start(request))

    async def _arun(
        self,
        url: str,
        max_depth: int = 2,
        max_pages: int = 50,
        format: str = "markdown",
        allow_external: bool = False,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            url=url,
            max_depth=max_depth,
            max_pages=max_pages,
            format=format,
            allow_external=allow_external,
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
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        crawl_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.crawl.get(crawl_id))

    async def _arun(
        self,
        crawl_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
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
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        crawl_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.crawl.stop(crawl_id))

    async def _arun(
        self,
        crawl_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
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
    client: Optional[ScrapeGraphAI] = None
    api_key: str

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        return _make_client(values)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        crawl_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Client not initialized")
        return result_to_dict(self.client.crawl.resume(crawl_id))

    async def _arun(
        self,
        crawl_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        return self._run(
            crawl_id=crawl_id,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
