"""Integration tests for ScrapeGraph AI tools.

To run these tests, you need a ScrapeGraphAI API key.
You can get a test key from https://scrapegraphai.com

Set the SGAI_API_KEY environment variable to run these tests.
"""

import os
from typing import Type

import pytest
from dotenv import load_dotenv
from langchain_tests.integration_tests import ToolsIntegrationTests

from langchain_scrapegraph.tools import GetCreditsTool, SmartscraperTool

# Load environment variables from .env file
load_dotenv()


class TestSmartscraperToolIntegration(ToolsIntegrationTests):
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
            "user_prompt": "Extract the main heading.",
            "website_url": "https://example.com",
        }


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
