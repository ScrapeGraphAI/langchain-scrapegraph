from typing import Type
from unittest.mock import patch

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_scrapegraph.tools import (
    GetCreditsTool,
    MarkdownifyTool,
    SearchScraperTool,
    SmartScraperTool,
)
from tests.unit_tests.mocks import (
    MockClient,
    MockGetCreditsTool,
    MockMarkdownifyTool,
    MockSearchScraperTool,
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

    def test_invoke_with_html(self):
        """Test invoking the tool with HTML content."""
        tool = self.tool_constructor(**self.tool_constructor_params)
        result = tool.invoke(
            {
                "user_prompt": "Extract the main heading",
                "website_url": "https://example.com",
                "website_html": "<html><body><h1>Test</h1></body></html>",
            }
        )
        assert isinstance(result, dict)
        assert "main_heading" in result
        assert result["main_heading"] == "Test"


class TestSearchScraperToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[SearchScraperTool]:
        return MockSearchScraperTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.searchscraper.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "user_prompt": "What are the key features of Product X?",
        }

    def test_invoke_with_schema(self):
        """Test invoking the tool with a schema."""
        from typing import List

        from pydantic import BaseModel, Field

        class TestSchema(BaseModel):
            product: dict = Field(description="Product information")
            features: List[dict] = Field(description="List of features")
            reference_urls: List[str] = Field(description="Reference URLs")

        tool = self.tool_constructor(**self.tool_constructor_params)
        tool.llm_output_schema = TestSchema
        result = tool.invoke(self.tool_invoke_params_example)
        assert isinstance(result, dict)
        assert "product" in result
        assert "features" in result
        assert "reference_urls" in result
        assert isinstance(result["reference_urls"], list)


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
