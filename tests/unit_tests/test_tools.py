from typing import Type
from unittest.mock import patch

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_scrapegraph.tools import (
    GetCreditsTool,
    SmartscraperTool,
    SubmitFeedbackTool,
)
from tests.unit_tests.mocks import (
    MockGetCreditsTool,
    MockSmartscraperTool,
    MockSubmitFeedbackTool,
    MockSyncClient,
)


class TestSmartscraperToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[SmartscraperTool]:
        return MockSmartscraperTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch(
            "langchain_scrapegraph.tools.smartscraper.SyncClient", MockSyncClient
        ):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "user_prompt": "Extract the main heading",
            "website_url": "https://example.com",
        }


class TestGetCreditsToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[GetCreditsTool]:
        return MockGetCreditsTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.credits.SyncClient", MockSyncClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {}


class TestSubmitFeedbackToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[SubmitFeedbackTool]:
        return MockSubmitFeedbackTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.feedback.SyncClient", MockSyncClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "request_id": "test-request-id",
            "rating": 5,
            "feedback_text": "Test feedback",
        }
