from typing import Type
from unittest.mock import patch

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_scrapegraph.tools import (
    CrawlStartTool,
    ExtractTool,
    GetCreditsTool,
    MarkdownifyTool,
    MonitorCreateTool,
    ScrapeTool,
    SearchTool,
)
from tests.unit_tests.mocks import (
    MockClient,
    MockCrawlStartTool,
    MockExtractTool,
    MockGetCreditsTool,
    MockMarkdownifyTool,
    MockMonitorCreateTool,
    MockScrapeTool,
    MockSearchTool,
)


class TestExtractToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[ExtractTool]:
        return MockExtractTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.extract.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "url": "https://example.com",
            "prompt": "Extract the main heading",
        }


class TestExtractToolCustom:
    def test_invoke_basic(self):
        with patch("langchain_scrapegraph.tools.extract.Client", MockClient):
            tool = MockExtractTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {
                    "url": "https://example.com",
                    "prompt": "Extract the main heading",
                }
            )
            assert isinstance(result, dict)
            assert "main_heading" in result


class TestSearchToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[SearchTool]:
        return MockSearchTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.search.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "query": "What are the key features of Product X?",
        }


class TestSearchToolCustom:
    def test_invoke_with_num_results(self):
        with patch("langchain_scrapegraph.tools.search.Client", MockClient):
            tool = MockSearchTool(api_key="sgai-test-api-key")
            result = tool.invoke({"query": "AI news", "num_results": 10})
            assert isinstance(result, dict)
            assert "results" in result


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


class TestScrapeToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[ScrapeTool]:
        return MockScrapeTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.scrape.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"url": "https://example.com"}


class TestScrapeToolCustom:
    def test_invoke_with_html_format(self):
        with patch("langchain_scrapegraph.tools.scrape.Client", MockClient):
            tool = MockScrapeTool(api_key="sgai-test-api-key")
            result = tool.invoke({"url": "https://example.com", "format": "html"})
            assert isinstance(result, dict)
            assert "content" in result


class TestCrawlStartToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[CrawlStartTool]:
        return MockCrawlStartTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.crawl.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "url": "https://example.com",
            "depth": 2,
            "max_pages": 10,
        }


class TestCrawlStartToolCustom:
    def test_invoke_basic(self):
        with patch("langchain_scrapegraph.tools.crawl.Client", MockClient):
            tool = MockCrawlStartTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {"url": "https://example.com", "depth": 3, "max_pages": 5}
            )
            assert isinstance(result, dict)
            assert "id" in result
            assert result["status"] == "running"


class TestMonitorCreateToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[MonitorCreateTool]:
        return MockMonitorCreateTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.monitor.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "name": "Test Monitor",
            "url": "https://example.com",
            "prompt": "Extract product prices",
            "cron": "0 9 * * *",
        }


class TestMonitorCreateToolCustom:
    def test_create_monitor(self):
        with patch("langchain_scrapegraph.tools.monitor.Client", MockClient):
            tool = MockMonitorCreateTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {
                    "name": "Price Monitor",
                    "url": "https://example.com",
                    "prompt": "Extract product prices",
                    "cron": "0 9 * * *",
                }
            )
            assert isinstance(result, dict)
            assert "id" in result
            assert result["status"] == "active"
