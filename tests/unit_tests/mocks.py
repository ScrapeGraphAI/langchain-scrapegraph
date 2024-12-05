from typing import Any, Dict, Optional

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockClient:
    def __init__(self, api_key: str = None, *args, **kwargs):
        """Initialize with mock methods that return proper response structures"""
        self._api_key = api_key

    def smartscraper(self, website_url: str, user_prompt: str) -> dict:
        """Mock smartscraper method"""
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

    def localscraper(self, website_html: str, user_prompt: str) -> dict:
        """Mock localscraper method"""
        return {
            "request_id": "test-id",
            "status": "completed",
            "user_prompt": user_prompt,
            "result": {
                "summary": "This is a technology company",
                "contact": {"email": "contact@example.com", "phone": "(555) 123-4567"},
            },
            "error": "",
        }

    def close(self) -> None:
        """Mock close method"""
        pass


class MockSmartScraperInput(BaseModel):
    user_prompt: str = Field(description="Test prompt")
    website_url: str = Field(description="Test URL")


class MockMarkdownifyInput(BaseModel):
    website_url: str = Field(description="Test URL")


class MockLocalScraperInput(BaseModel):
    user_prompt: str = Field(description="Test prompt")
    website_html: str = Field(description="Test HTML")


class MockSmartScraperTool(BaseTool):
    name: str = "SmartScraper"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockSmartScraperInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"main_heading": "Test", "first_paragraph": "Test"}


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


class MockLocalScraperTool(BaseTool):
    name: str = "LocalScraper"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockLocalScraperInput
    client: Optional[MockClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "summary": "This is a technology company",
            "contact": {"email": "contact@example.com", "phone": "(555) 123-4567"},
        }
