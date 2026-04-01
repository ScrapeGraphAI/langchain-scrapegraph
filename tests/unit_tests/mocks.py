from typing import Any, Dict, List, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockCrawlNamespace:
    def __init__(self, client):
        self._client = client

    def start(
        self,
        url: str,
        depth: int = 2,
        max_pages: int = 10,
        format: str = "markdown",
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        fetch_config=None,
    ) -> dict:
        return {
            "id": "crawl-job-123",
            "status": "running",
            "url": url,
            "depth": depth,
            "max_pages": max_pages,
        }

    def status(self, crawl_id: str) -> dict:
        return {
            "id": crawl_id,
            "status": "completed",
            "pages_crawled": 5,
            "results": [{"url": "https://example.com", "content": "# Example"}],
        }

    def stop(self, crawl_id: str) -> dict:
        return {"id": crawl_id, "status": "stopped"}

    def resume(self, crawl_id: str) -> dict:
        return {"id": crawl_id, "status": "running"}


class MockMonitorNamespace:
    def __init__(self, client):
        self._client = client

    def create(
        self,
        name: str,
        url: str,
        prompt: str,
        cron: str,
        output_schema=None,
        fetch_config=None,
        llm_config=None,
    ) -> dict:
        return {
            "id": "monitor-123",
            "name": name,
            "url": url,
            "prompt": prompt,
            "cron": cron,
            "status": "active",
        }

    def list(self) -> dict:
        return {
            "monitors": [
                {
                    "id": "monitor-123",
                    "name": "Test Monitor",
                    "url": "https://example.com",
                    "status": "active",
                }
            ]
        }

    def get(self, monitor_id: str) -> dict:
        return {
            "id": monitor_id,
            "name": "Test Monitor",
            "url": "https://example.com",
            "status": "active",
        }

    def pause(self, monitor_id: str) -> dict:
        return {"id": monitor_id, "status": "paused"}

    def resume(self, monitor_id: str) -> dict:
        return {"id": monitor_id, "status": "active"}

    def delete(self, monitor_id: str) -> dict:
        return {"message": "Monitor deleted successfully", "id": monitor_id}


class MockClient:
    def __init__(self, api_key: str = None, *args, **kwargs):
        self._api_key = api_key
        self.crawl = MockCrawlNamespace(self)
        self.monitor = MockMonitorNamespace(self)

    def extract(
        self,
        url: str,
        prompt: str,
        output_schema=None,
        fetch_config=None,
        llm_config=None,
    ) -> dict:
        return {
            "id": "test-id",
            "data": {
                "main_heading": "Example Domain",
                "first_paragraph": "Test paragraph",
            },
        }

    def search(
        self,
        query: str,
        num_results: int = 5,
        output_schema=None,
        llm_config=None,
    ) -> dict:
        return {
            "id": "test-id",
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://example.com",
                    "content": "Test content",
                }
            ],
        }

    def scrape(self, url: str, format: str = "markdown", fetch_config=None) -> dict:
        if format == "html":
            return {
                "id": "test-id",
                "format": "html",
                "content": ["<html><body><h1>Example Domain</h1></body></html>"],
            }
        return {
            "id": "test-id",
            "format": "markdown",
            "content": ["# Example Domain\n\nTest paragraph"],
        }

    def credits(self) -> dict:
        return {"remaining_credits": 50, "total_credits_used": 543}

    def history(
        self,
        endpoint: str = None,
        status: str = None,
        limit: int = None,
        offset: int = None,
    ) -> dict:
        return {
            "requests": [
                {
                    "id": "req-123",
                    "endpoint": "scrape",
                    "status": "completed",
                    "created_at": "2024-01-01T00:00:00Z",
                }
            ],
            "total": 1,
        }

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
    num_results: int = Field(default=5, description="Number of results")


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
        return {"remaining_credits": 50, "total_credits_used": 543}


class MockMarkdownifyInput(BaseModel):
    website_url: str = Field(description="Test URL")


class MockMarkdownifyTool(BaseTool):
    name: str = "Markdownify"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockMarkdownifyInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "id": "test-id",
            "format": "markdown",
            "content": ["# Example Domain\n\nTest paragraph"],
        }


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
        return {
            "id": "test-id",
            "format": "markdown",
            "content": ["# Example Domain\n\nTest paragraph"],
        }


class MockCrawlStartInput(BaseModel):
    url: str = Field(description="Test URL")
    depth: int = Field(default=2, description="Crawl depth")
    max_pages: int = Field(default=10, description="Max pages")
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
    name: str = Field(description="Monitor name")
    url: str = Field(description="Monitor URL")
    prompt: str = Field(description="Monitor prompt")
    cron: str = Field(description="Cron expression")


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
