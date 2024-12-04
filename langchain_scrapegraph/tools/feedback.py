from typing import Any, Dict, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from scrapegraph_py import SyncClient


class SubmitFeedbackInput(BaseModel):
    request_id: str = Field(description="The ID of the request to provide feedback for")
    rating: int = Field(description="Rating from 1-5", ge=1, le=5)
    feedback_text: str = Field(description="Detailed feedback text")


class SubmitFeedbackTool(BaseTool):
    name: str = "SubmitFeedback"
    description: str = "Submit feedback for a previous ScrapeGraph AI request"
    args_schema: Type[SubmitFeedbackInput] = SubmitFeedbackInput
    return_direct: bool = True
    client: Optional[SyncClient] = None
    api_key: str
    testing: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["api_key"] = get_from_dict_or_env(values, "api_key", "SGAI_API_KEY")
        values["client"] = SyncClient(api_key=values["api_key"])
        return values

    def __init__(self, **data: Any):
        super().__init__(**data)

    def _run(
        self,
        request_id: str,
        rating: int,
        feedback_text: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        """Submit feedback for a request."""
        if not self.client:
            raise ValueError("Client not initialized")
        return self.client.submit_feedback(
            request_id=request_id, rating=rating, feedback_text=feedback_text
        )

    async def _arun(
        self,
        request_id: str,
        rating: int,
        feedback_text: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> dict:
        """Submit feedback asynchronously."""
        return self._run(
            request_id=request_id,
            rating=rating,
            feedback_text=feedback_text,
            run_manager=run_manager.get_sync() if run_manager else None,
        )
