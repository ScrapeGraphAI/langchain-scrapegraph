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
