from typing import Type
from unittest.mock import patch

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_scrapegraph.tools import (
    CreateScheduledJobTool,
    GetCreditsTool,
    GetScheduledJobsTool,
    MarkdownifyTool,
    ScrapeTool,
    SearchScraperTool,
    SmartScraperTool,
)
from tests.unit_tests.mocks import (
    MockClient,
    MockCreateScheduledJobTool,
    MockGetCreditsTool,
    MockGetScheduledJobsTool,
    MockMarkdownifyTool,
    MockScrapeTool,
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


class TestSmartScraperToolCustom:
    def test_invoke_with_html(self):
        """Test invoking the tool with HTML content."""
        with patch("langchain_scrapegraph.tools.smartscraper.Client", MockClient):
            tool = MockSmartScraperTool(api_key="sgai-test-api-key")
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


class TestSearchScraperToolCustom:
    def test_invoke_with_schema(self):
        """Test invoking the tool with a schema."""
        from typing import List

        from pydantic import BaseModel, Field

        class TestSchema(BaseModel):
            product: dict = Field(description="Product information")
            features: List[dict] = Field(description="List of features")
            reference_urls: List[str] = Field(description="Reference URLs")

        with patch("langchain_scrapegraph.tools.searchscraper.Client", MockClient):
            tool = MockSearchScraperTool(api_key="sgai-test-api-key")
            tool.llm_output_schema = TestSchema
            result = tool.invoke(
                {"user_prompt": "What are the key features of Product X?"}
            )
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
        return {"website_url": "https://example.com"}


class TestScrapeToolCustom:
    def test_invoke_with_js_rendering(self):
        """Test invoking the scrape tool with JavaScript rendering."""
        with patch("langchain_scrapegraph.tools.scrape.Client", MockClient):
            tool = MockScrapeTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {"website_url": "https://example.com", "render_heavy_js": True}
            )
            assert isinstance(result, dict)
            assert "html" in result
            assert "scrape_request_id" in result
            assert result["status"] == "success"

    def test_invoke_with_headers(self):
        """Test invoking the scrape tool with custom headers."""
        with patch("langchain_scrapegraph.tools.scrape.Client", MockClient):
            tool = MockScrapeTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {
                    "website_url": "https://example.com",
                    "headers": {"User-Agent": "Test Bot 1.0"},
                }
            )
            assert isinstance(result, dict)
            assert "html" in result
            assert result["status"] == "success"


class TestCreateScheduledJobToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[CreateScheduledJobTool]:
        return MockCreateScheduledJobTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.scheduled_jobs.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "job_name": "Test Job",
            "service_type": "smartscraper",
            "cron_expression": "0 9 * * *",
            "job_config": {"website_url": "https://example.com", "user_prompt": "test"},
            "is_active": True,
        }


class TestCreateScheduledJobToolCustom:
    def test_create_smartscraper_job(self):
        """Test creating a SmartScraper scheduled job."""
        with patch("langchain_scrapegraph.tools.scheduled_jobs.Client", MockClient):
            tool = MockCreateScheduledJobTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {
                    "job_name": "Daily Scraping Job",
                    "service_type": "smartscraper",
                    "cron_expression": "0 9 * * *",
                    "job_config": {
                        "website_url": "https://example.com",
                        "user_prompt": "Extract the main heading",
                    },
                    "is_active": True,
                }
            )
            assert isinstance(result, dict)
            assert result["job_name"] == "Daily Scraping Job"
            assert result["service_type"] == "smartscraper"
            assert result["is_active"] is True
            assert "id" in result

    def test_create_searchscraper_job(self):
        """Test creating a SearchScraper scheduled job."""
        with patch("langchain_scrapegraph.tools.scheduled_jobs.Client", MockClient):
            tool = MockCreateScheduledJobTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {
                    "job_name": "Weekly Search Job",
                    "service_type": "searchscraper",
                    "cron_expression": "0 10 * * 1",
                    "job_config": {
                        "user_prompt": "Find latest AI news",
                        "num_results": 5,
                    },
                    "is_active": True,
                }
            )
            assert isinstance(result, dict)
            assert result["job_name"] == "Weekly Search Job"
            assert result["service_type"] == "searchscraper"


class TestGetScheduledJobsToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[GetScheduledJobsTool]:
        return MockGetScheduledJobsTool

    @property
    def tool_constructor_params(self) -> dict:
        with patch("langchain_scrapegraph.tools.scheduled_jobs.Client", MockClient):
            return {"api_key": "sgai-test-api-key"}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"page": 1, "page_size": 10}


class TestGetScheduledJobsToolCustom:
    def test_get_jobs_with_filters(self):
        """Test getting scheduled jobs with filters."""
        with patch("langchain_scrapegraph.tools.scheduled_jobs.Client", MockClient):
            tool = MockGetScheduledJobsTool(api_key="sgai-test-api-key")
            result = tool.invoke(
                {
                    "page": 1,
                    "page_size": 10,
                    "service_type": "smartscraper",
                    "is_active": True,
                }
            )
            assert isinstance(result, dict)
            assert "jobs" in result
            assert "total" in result
            assert isinstance(result["jobs"], list)
