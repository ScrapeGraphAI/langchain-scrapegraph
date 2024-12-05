from typing import Type
from unittest.mock import patch

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_scrapegraph.tools import (
    GetCreditsTool,
    LocalScraperTool,
    MarkdownifyTool,
    SmartScraperTool,
)
from tests.unit_tests.mocks import (
    MockClient,
    MockGetCreditsTool,
    MockLocalScraperTool,
    MockMarkdownifyTool,
    MockSmartScraperTool,
)


class TestSmartScraperToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[SmartScraperTool]:
        return MockSmartScraperTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.smartscraper.Client", MockClient):
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
        with patch("langchain_scrapegraph.tools.credits.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {}


class TestMarkdownifyToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[MarkdownifyTool]:
        return MockMarkdownifyTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.markdownify.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"website_url": "https://example.com"}


class TestLocalScraperToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[LocalScraperTool]:
        return MockLocalScraperTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.localscraper.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "user_prompt": "Make a summary and extract contact info",
            "website_html": "<html><body><h1>Test</h1></body></html>",
        }
