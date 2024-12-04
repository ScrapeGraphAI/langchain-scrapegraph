from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockSyncClient:
    def __init__(self, api_key: str = None, *args, **kwargs):
        """Initialize with mock methods that return proper response structures"""
        self._api_key = api_key
        self._request_id = str(uuid4())  # Generate a consistent request_id for tests

    def smartscraper(self, website_url: str, user_prompt: str) -> dict:
        """Mock smartscraper method"""
        return {
            "request_id": self._request_id,
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

    def submit_feedback(self, request_id: str, rating: int, feedback_text: str) -> dict:
        """Mock submit_feedback method"""
        return {
            "feedback_id": str(uuid4()),
            "request_id": request_id,
            "message": "Feedback submitted successfully",
            "feedback_timestamp": datetime.now().isoformat(),
        }

    def close(self) -> None:
        """Mock close method"""
        pass


class MockSmartscraperInput(BaseModel):
    user_prompt: str = Field(description="Test prompt")
    website_url: str = Field(description="Test URL")


class MockSmartscraperTool(BaseTool):
    name: str = "Smartscraper"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockSmartscraperInput
    client: Optional[MockSyncClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"main_heading": "Test", "first_paragraph": "Test"}


class MockGetCreditsTool(BaseTool):
    name: str = "GetCredits"
    description: str = "Test description"
    client: Optional[MockSyncClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {"remaining_credits": 50, "total_credits_used": 543}


class MockSubmitFeedbackInput(BaseModel):
    request_id: str = Field(description="Test request ID")
    rating: int = Field(description="Test rating")
    feedback_text: str = Field(description="Test feedback")


class MockSubmitFeedbackTool(BaseTool):
    name: str = "SubmitFeedback"
    description: str = "Test description"
    args_schema: type[BaseModel] = MockSubmitFeedbackInput
    client: Optional[MockSyncClient] = None
    api_key: str

    def _run(self, **kwargs: Any) -> Dict:
        return {
            "feedback_id": "test-id",
            "message": "Success",
            "feedback_timestamp": "2024-01-01T00:00:00",
        }
