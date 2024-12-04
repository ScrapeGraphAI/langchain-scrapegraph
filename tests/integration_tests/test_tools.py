"""Integration tests for ScrapeGraph AI tools.

To run these tests, you need a ScrapeGraph AI API key.
You can get a test key from https://scrapegraphai.com

Set the SGAI_API_KEY environment variable to run these tests.
"""

import os
from typing import ClassVar, Type

import pytest
from dotenv import load_dotenv
from langchain_tests.integration_tests import ToolsIntegrationTests

from langchain_scrapegraph.tools import (
    GetCreditsTool,
    SmartscraperTool,
    SubmitFeedbackTool,
)

# Load environment variables from .env file
load_dotenv()


class TestSmartscraperToolIntegration(ToolsIntegrationTests):
    request_id: ClassVar[str] = ""  # Class variable to store request_id

    @property
    def tool_constructor(self) -> Type[SmartscraperTool]:
        return SmartscraperTool

    @property
    def tool_constructor_params(self) -> dict:
        api_key = os.getenv("SGAI_API_KEY")
        if not api_key:
            pytest.skip("SGAI_API_KEY environment variable not set")
        return {"api_key": api_key}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "user_prompt": "TEST. Extract the main heading.",
            "website_url": "https://example.com",
        }

    @pytest.mark.xfail(reason="Overridden to capture request_id for feedback test")
    def test_invoke_matches_output_schema(self) -> None:
        """Override to capture request_id"""
        tool = self.get_tool()
        result = tool._run(**self.tool_invoke_params_example)
        # Store the request_id for use in feedback test
        TestSmartscraperToolIntegration.request_id = result.get("request_id", "")
        assert isinstance(result, dict)


class TestGetCreditsToolIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[GetCreditsTool]:
        return GetCreditsTool

    @property
    def tool_constructor_params(self) -> dict:
        api_key = os.getenv("SGAI_API_KEY")
        if not api_key:
            pytest.skip("SGAI_API_KEY environment variable not set")
        return {"api_key": api_key}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {}  # GetCredits doesn't require any parameters


class TestSubmitFeedbackToolIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[SubmitFeedbackTool]:
        return SubmitFeedbackTool

    @property
    def tool_constructor_params(self) -> dict:
        api_key = os.getenv("SGAI_API_KEY")
        if not api_key:
            pytest.skip("SGAI_API_KEY environment variable not set")
        return {"api_key": api_key}

    @property
    def tool_invoke_params_example(self) -> dict:
        if not TestSmartscraperToolIntegration.request_id:
            pytest.skip("No request_id available from smartscraper test")
        return {
            "request_id": TestSmartscraperToolIntegration.request_id,
            "rating": 5,
            "feedback_text": "Test feedback",
        }
