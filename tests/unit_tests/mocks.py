from typing import Any, Dict, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


def _api_result(data: dict) -> dict:
    return {"status": "success", "data": data, "error": None, "elapsed_ms": 0}


class _HasModelDump:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def model_dump(self, **_kwargs: Any) -> dict:
        return self._payload


class MockCrawlResource:
    def __init__(self, client: "MockClient") -> None:
        self._client = client

    def start(self, request: Any) -> Any:
        params = (
            request.model_dump(by_alias=False)
            if hasattr(request, "model_dump")
            else dict(request)
        )
        return _HasModelDump(
            _api_result(
                {
                    "id": "crawl-job-123",
                    "status": "running",
                    "url": str(params.get("url", "")),
                    "max_depth": params.get("max_depth", 2),
                    "max_pages": params.get("max_pages", 50),
                }
            )
        )

    def get(self, crawl_id: str) -> Any:
        return _HasModelDump(
            _api_result(
                {
                    "id": crawl_id,
                    "status": "completed",
                    "total": 5,
                    "finished": 5,
                    "pages": [{"url": "https://example.com", "status": "completed"}],
                }
            )
        )

    def stop(self, crawl_id: str) -> Any:
        return _HasModelDump(_api_result({"id": crawl_id, "status": "stopped"}))

    def resume(self, crawl_id: str) -> Any:
        return _HasModelDump(_api_result({"id": crawl_id, "status": "running"}))


class MockMonitorResource:
    def __init__(self, client: "MockClient") -> None:
        self._client = client

    def create(self, request: Any) -> Any:
        params = (
            request.model_dump(by_alias=False)
            if hasattr(request, "model_dump")
            else dict(request)
        )
        return _HasModelDump(
            _api_result(
                {
                    "id": "monitor-123",
                    "name": params.get("name"),
                    "url": str(params.get("url", "")),
                    "interval": params.get("interval"),
                    "status": "active",
                }
            )
        )

    def list(self) -> Any:
        return _HasModelDump(
            _api_result(
                [
                    {
                        "id": "monitor-123",
                        "name": "Test Monitor",
                        "url": "https://example.com",
                        "status": "active",
                    }
                ]
            )
        )

    def get(self, monitor_id: str) -> Any:
        return _HasModelDump(
            _api_result(
                {
                    "id": monitor_id,
                    "name": "Test Monitor",
                    "url": "https://example.com",
                    "status": "active",
                }
            )
        )

    def pause(self, monitor_id: str) -> Any:
        return _HasModelDump(_api_result({"id": monitor_id, "status": "paused"}))

    def resume(self, monitor_id: str) -> Any:
        return _HasModelDump(_api_result({"id": monitor_id, "status": "active"}))

    def delete(self, monitor_id: str) -> Any:
        return _HasModelDump(_api_result({"id": monitor_id, "deleted": True}))


class MockHistoryResource:
    def __init__(self, client: "MockClient") -> None:
        self._client = client

    def list(self, filter: Any) -> Any:
        return _HasModelDump(
            _api_result(
                {
                    "data": [
                        {
                            "id": "req-123",
                            "service": "scrape",
                            "status": "completed",
                            "created_at": "2024-01-01T00:00:00Z",
                        }
                    ],
                    "pagination": {"page": 1, "limit": 20, "total": 1},
                }
            )
        )

    def get(self, entry_id: str) -> Any:
        return _HasModelDump(
            _api_result(
                {
                    "id": entry_id,
                    "service": "scrape",
                    "status": "completed",
                }
            )
        )


class MockClient:
    def __init__(self, *, api_key: Optional[str] = None, **_kwargs: Any) -> None:
        self._api_key = api_key
        self.crawl = MockCrawlResource(self)
        self.monitor = MockMonitorResource(self)
        self.history = MockHistoryResource(self)

    def scrape(self, request: Any) -> Any:
        params = (
            request.model_dump(by_alias=False)
            if hasattr(request, "model_dump")
            else dict(request)
        )
        formats = params.get("formats") or []
        first = formats[0] if formats else {"type": "markdown"}
        if isinstance(first, dict):
            fmt = first.get("type", "markdown")
        else:
            fmt = getattr(first, "type", "markdown")
        body = (
            {"markdown": "# Example Domain\n"}
            if fmt == "markdown"
            else {fmt: "<html><body><h1>Example Domain</h1></body></html>"}
        )
        return _HasModelDump(
            _api_result(
                {
                    "results": body,
                    "metadata": {"provider": "mock", "content_type": "text/html"},
                }
            )
        )

    def extract(self, request: Any) -> Any:
        params = (
            request.model_dump(by_alias=False)
            if hasattr(request, "model_dump")
            else dict(request)
        )
        return _HasModelDump(
            _api_result(
                {
                    "raw": None,
                    "json": {
                        "main_heading": "Example Domain",
                        "first_paragraph": "Test paragraph",
                    },
                    "usage": {"prompt_tokens": 10, "completion_tokens": 5},
                    "metadata": {"prompt": params.get("prompt")},
                }
            )
        )

    def search(self, request: Any) -> Any:
        params = (
            request.model_dump(by_alias=False)
            if hasattr(request, "model_dump")
            else dict(request)
        )
        return _HasModelDump(
            _api_result(
                {
                    "results": [
                        {
                            "url": "https://example.com",
                            "title": "Test Result",
                            "content": "Test content",
                        }
                    ],
                    "metadata": {
                        "search": {"query": params.get("query")},
                        "pages": {"count": 1},
                    },
                }
            )
        )

    def credits(self) -> Any:
        return _HasModelDump(
            _api_result(
                {
                    "remaining": 50,
                    "used": 543,
                    "plan": "pro",
                    "jobs": {
                        "crawl": {"used": 0, "limit": 10},
                        "monitor": {"used": 0, "limit": 10},
                    },
                }
            )
        )

    def health(self) -> Any:
        return _HasModelDump(_api_result({"status": "ok", "uptime": 1}))

    def close(self) -> None:
        pass


class MockExtractInput(BaseModel):
    url: str = Field(description="Test URL")
    prompt: str = Field(description="Test prompt")


class MockExtractTool(BaseTool):
    name: str = "Extract"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockExtractInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"main_heading": "Test", "first_paragraph": "Test"}


class MockSearchInput(BaseModel):
    query: str = Field(description="Test query")
    num_results: int = Field(default=3, description="Number of results")


class MockSearchTool(BaseTool):
    name: str = "Search"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockSearchInput
    client: Optional[MockClient] = None
    api_key: str
    llm_output_schema: Optional[Type[BaseModel]] = None

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://example.com",
                    "content": "Test",
                }
            ],
        }


class MockGetCreditsTool(BaseTool):
    name: str = "GetCredits"
    description: str = "Test description"
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"remaining": 50, "used": 543}


class MockMarkdownifyInput(BaseModel):
    website_url: str = Field(description="Test URL")


class MockMarkdownifyTool(BaseTool):
    name: str = "Markdownify"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockMarkdownifyInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"results": {"markdown": "# Example Domain\n"}}


class MockScrapeInput(BaseModel):
    url: str = Field(description="Test URL")
    format: str = Field(default="markdown", description="Output format")


class MockScrapeTool(BaseTool):
    name: str = "Scrape"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockScrapeInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        fmt = kwargs.get("format", "markdown")
        body = (
            {"markdown": "# Example Domain\n"} if fmt == "markdown" else {fmt: "data"}
        )
        return {"results": body}


class MockCrawlStartInput(BaseModel):
    url: str = Field(description="Test URL")
    max_depth: int = Field(default=2, description="Crawl depth")
    max_pages: int = Field(default=50, description="Max pages")
    format: str = Field(default="markdown", description="Output format")


class MockCrawlStartTool(BaseTool):
    name: str = "CrawlStart"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockCrawlStartInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "id": "crawl-job-123",
            "status": "running",
            "url": kwargs.get("url", "https://example.com"),
        }


class MockMonitorCreateInput(BaseModel):
    url: str = Field(description="Monitor URL")
    interval: str = Field(description="Monitor interval")
    name: Optional[str] = Field(default=None, description="Monitor name")
    prompt: Optional[str] = Field(default=None, description="Monitor prompt")


class MockMonitorCreateTool(BaseTool):
    name: str = "MonitorCreate"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockMonitorCreateInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "id": "monitor-123",
            "name": kwargs.get("name", "Test Monitor"),
            "url": kwargs.get("url", "https://example.com"),
            "status": "active",
        }
