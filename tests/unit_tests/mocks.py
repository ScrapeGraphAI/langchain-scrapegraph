from typing import Any, Dict, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockClient:
    def __init__(self, api_key: str = None, *args, **kwargs):
        """Initialize with mock methods that return proper response structures"""
        self._api_key = api_key

    def smartscraper(
        self, website_url: str, user_prompt: str, website_html: str = None
    ) -> dict:
        """Mock smartscraper method"""
        # If website_html is provided, use it to determine the response
        if website_html and "<h1>Test</h1>" in website_html:
            return {
                "request_id": "test-id",
                "status": "completed",
                "website_url": website_url,
                "user_prompt": user_prompt,
                "result": {
                    "main_heading": "Test",
                    "first_paragraph": "Test paragraph",
                },
                "error": "",
            }

        # Default response for URL-based requests
        return {
            "request_id": "test-id",
            "status": "completed",
            "website_url": website_url,
            "user_prompt": user_prompt,
            "result": {
                "main_heading": "Example Domain",
                "first_paragraph": "Test paragraph",
            },
            "error": "",
        }

    def searchscraper(self, user_prompt: str) -> dict:
        """Mock searchscraper method"""
        return {
            "request_id": "test-id",
            "status": "completed",
            "user_prompt": user_prompt,
            "result": {
                "product": {"name": "Test Product", "description": "Test description"},
                "features": [{"name": "Feature 1", "description": "Description 1"}],
                "pricing": {
                    "plans": [
                        {
                            "name": "Basic Plan",
                            "price": {
                                "amount": "10",
                                "currency": "USD",
                                "period": "monthly",
                            },
                        }
                    ]
                },
            },
            "reference_urls": ["https://example.com/test"],
            "error": "",
        }

    def get_credits(self) -> dict:
        """Mock get_credits method"""
        return {"remaining_credits": 50, "total_credits_used": 543}

    def markdownify(self, website_url: str) -> dict:
        """Mock markdownify method"""
        return {
            "request_id": "test-id",
            "status": "completed",
            "website_url": website_url,
            "result": "# Example Domain\n\nTest paragraph",
            "error": "",
        }

    def scrape(
        self, website_url: str, render_heavy_js: bool = False, headers: dict = None
    ) -> dict:
        """Mock scrape method"""
        return {
            "scrape_request_id": "test-scrape-id",
            "status": "success",
            "html": "<html><body><h1>Example Domain</h1><p>Test content</p></body></html>",
            "error": None,
        }

    def create_scheduled_job(
        self,
        job_name: str,
        service_type: str,
        cron_expression: str,
        job_config: dict,
        is_active: bool = True,
    ) -> dict:
        """Mock create_scheduled_job method"""
        return {
            "id": "test-job-id-123",
            "job_name": job_name,
            "service_type": service_type,
            "cron_expression": cron_expression,
            "job_config": job_config,
            "is_active": is_active,
            "created_at": "2024-01-01T00:00:00Z",
            "next_run_at": "2024-01-02T09:00:00Z",
        }

    def get_scheduled_jobs(
        self,
        page: int = 1,
        page_size: int = 10,
        service_type: str = None,
        is_active: bool = None,
    ) -> dict:
        """Mock get_scheduled_jobs method"""
        jobs = [
            {
                "id": "test-job-1",
                "job_name": "Test Job 1",
                "service_type": "smartscraper",
                "cron_expression": "0 9 * * *",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "next_run_at": "2024-01-02T09:00:00Z",
            }
        ]

        # Apply filters
        if service_type:
            jobs = [job for job in jobs if job["service_type"] == service_type]
        if is_active is not None:
            jobs = [job for job in jobs if job["is_active"] == is_active]

        return {"jobs": jobs, "total": len(jobs), "page": page, "page_size": page_size}

    def get_scheduled_job(self, job_id: str) -> dict:
        """Mock get_scheduled_job method"""
        return {
            "id": job_id,
            "job_name": "Test Job",
            "service_type": "smartscraper",
            "cron_expression": "0 9 * * *",
            "job_config": {"website_url": "https://example.com", "user_prompt": "test"},
            "is_active": True,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "next_run_at": "2024-01-02T09:00:00Z",
        }

    def update_scheduled_job(
        self,
        job_id: str,
        job_name: str = None,
        cron_expression: str = None,
        job_config: dict = None,
        is_active: bool = None,
    ) -> dict:
        """Mock update_scheduled_job method"""
        return {
            "id": job_id,
            "job_name": job_name or "Updated Test Job",
            "service_type": "smartscraper",
            "cron_expression": cron_expression or "0 8 * * *",
            "is_active": is_active if is_active is not None else True,
            "updated_at": "2024-01-01T00:00:00Z",
        }

    def pause_scheduled_job(self, job_id: str) -> dict:
        """Mock pause_scheduled_job method"""
        return {
            "message": "Job paused successfully",
            "job_id": job_id,
            "is_active": False,
        }

    def resume_scheduled_job(self, job_id: str) -> dict:
        """Mock resume_scheduled_job method"""
        return {
            "message": "Job resumed successfully",
            "job_id": job_id,
            "is_active": True,
            "next_run_at": "2024-01-02T09:00:00Z",
        }

    def trigger_scheduled_job(self, job_id: str) -> dict:
        """Mock trigger_scheduled_job method"""
        return {
            "message": "Job triggered successfully",
            "job_id": job_id,
            "execution_id": "exec-123",
            "triggered_at": "2024-01-01T12:00:00Z",
        }

    def get_job_executions(
        self, job_id: str, page: int = 1, page_size: int = 10
    ) -> dict:
        """Mock get_job_executions method"""
        executions = [
            {
                "id": "exec-1",
                "job_id": job_id,
                "status": "completed",
                "started_at": "2024-01-01T09:00:00Z",
                "completed_at": "2024-01-01T09:01:00Z",
                "credits_used": 1,
            }
        ]
        return {
            "executions": executions,
            "total": len(executions),
            "page": page,
            "page_size": page_size,
        }

    def delete_scheduled_job(self, job_id: str) -> dict:
        """Mock delete_scheduled_job method"""
        return {"message": "Job deleted successfully", "job_id": job_id}

    def close(self) -> None:
        """Mock close method"""
        pass


class MockSmartScraperInput(BaseModel):
    user_prompt: str = Field(description="Test prompt")
    website_url: str = Field(description="Test URL")


class MockSearchScraperInput(BaseModel):
    user_prompt: str = Field(description="Test prompt")


class MockMarkdownifyInput(BaseModel):
    website_url: str = Field(description="Test URL")


class MockSmartScraperTool(BaseTool):
    name: str = "SmartScraper"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockSmartScraperInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"main_heading": "Test", "first_paragraph": "Test"}


class MockSearchScraperTool(BaseTool):
    name: str = "SearchScraper"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockSearchScraperInput
    client: Optional[MockClient] = None
    api_key: str
    llm_output_schema: Optional[Type[BaseModel]] = None

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "product": {"name": "Test Product", "description": "Test description"},
            "features": [{"name": "Feature 1", "description": "Description 1"}],
            "reference_urls": ["https://example.com/test"],
        }


class MockGetCreditsTool(BaseTool):
    name: str = "GetCredits"
    description: str = "Test description"
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"remaining_credits": 50, "total_credits_used": 543}


class MockMarkdownifyTool(BaseTool):
    name: str = "Markdownify"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockMarkdownifyInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> str:
        return "# Example Domain\n\nTest paragraph"


class MockScrapeInput(BaseModel):
    website_url: str = Field(description="Test URL")
    render_heavy_js: bool = Field(default=False, description="Test JS rendering")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Test headers")


class MockScrapeTool(BaseTool):
    name: str = "Scrape"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockScrapeInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "scrape_request_id": "test-scrape-id",
            "status": "success",
            "html": "<html><body><h1>Example Domain</h1><p>Test content</p></body></html>",
            "error": None,
        }


class MockCreateScheduledJobInput(BaseModel):
    job_name: str = Field(description="Test job name")
    service_type: str = Field(description="Test service type")
    cron_expression: str = Field(description="Test cron expression")
    job_config: Dict[str, Any] = Field(description="Test job config")
    is_active: bool = Field(default=True, description="Test active status")


class MockCreateScheduledJobTool(BaseTool):
    name: str = "CreateScheduledJob"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockCreateScheduledJobInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "id": "test-job-id-123",
            "job_name": kwargs.get("job_name", "Test Job"),
            "service_type": kwargs.get("service_type", "smartscraper"),
            "cron_expression": kwargs.get("cron_expression", "0 9 * * *"),
            "job_config": kwargs.get("job_config", {}),
            "is_active": kwargs.get("is_active", True),
            "created_at": "2024-01-01T00:00:00Z",
            "next_run_at": "2024-01-02T09:00:00Z",
        }


class MockGetScheduledJobsInput(BaseModel):
    page: int = Field(default=1, description="Test page")
    page_size: int = Field(default=10, description="Test page size")
    service_type: Optional[str] = Field(default=None, description="Test service type")
    is_active: Optional[bool] = Field(default=None, description="Test active status")


class MockGetScheduledJobsTool(BaseTool):
    name: str = "GetScheduledJobs"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockGetScheduledJobsInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        jobs = [
            {
                "id": "test-job-1",
                "job_name": "Test Job 1",
                "service_type": "smartscraper",
                "cron_expression": "0 9 * * *",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "next_run_at": "2024-01-02T09:00:00Z",
            }
        ]
        return {"jobs": jobs, "total": len(jobs), "page": 1, "page_size": 10}
