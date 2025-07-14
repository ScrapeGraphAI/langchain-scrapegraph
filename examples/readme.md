# LangChain ScrapeGraph Examples

This directory contains comprehensive examples demonstrating how to use the LangChain ScrapeGraph tools for web scraping and data extraction.

## Prerequisites

Before running these examples, make sure you have:

1. **API Key**: Set your ScrapeGraph AI API key as an environment variable:
   ```bash
   export SGAI_API_KEY="your-api-key-here"
   ```

2. **Dependencies**: Install the required packages:
   ```bash
   pip install langchain-scrapegraph scrapegraph-py
   ```

   For the agent example, you'll also need:
   ```bash
   pip install langchain-openai langchain python-dotenv
   ```

## Available Examples

### 1. Agent Integration (`agent_example.py`)
**Purpose**: Demonstrates how to integrate ScrapeGraph tools with a LangChain agent for conversational web scraping.

**Features**:
- Uses OpenAI's function calling capabilities
- Combines multiple tools (SmartScraper, GetCredits, SearchScraper)
- Provides conversational interface for web scraping tasks
- Includes verbose output to show agent reasoning

**Usage**:
```python
python agent_example.py
```

### 2. Basic Tool Examples

#### Get Credits Tool (`get_credits_tool.py`)
**Purpose**: Check your remaining API credits.

**Features**:
- Simple API credit checking
- No parameters required
- Returns current credit balance

**Usage**:
```python
python get_credits_tool.py
```

#### Markdownify Tool (`markdownify_tool.py`)
**Purpose**: Convert website content to clean markdown format.

**Features**:
- Converts HTML to markdown
- Cleans and structures content
- Preserves formatting and links

**Usage**:
```python
python markdownify_tool.py
```

#### Smart Scraper Tool (`smartscraper_tool.py`)
**Purpose**: Extract specific information from a single webpage using AI.

**Features**:
- Target specific websites
- Use natural language prompts
- Extract structured data
- Support for both URL and HTML content

**Usage**:
```python
python smartscraper_tool.py
```

#### Search Scraper Tool (`searchscraper_tool.py`)
**Purpose**: Search the web and extract information based on a query.

**Features**:
- Web search capabilities
- AI-powered content extraction
- No specific URL required
- Returns relevant information from multiple sources

**Usage**:
```python
python searchscraper_tool.py
```

#### Smart Crawler Tool (`smartcrawler_tool.py`)
**Purpose**: Crawl multiple pages of a website and extract comprehensive information.

**Features**:
- Multi-page crawling
- Configurable depth and page limits
- Domain restriction options
- Website caching for efficiency
- Extract information from multiple related pages

**Usage**:
```python
python smartcrawler_tool.py
```

### 3. Structured Output Examples

All tools support structured output using Pydantic models. These examples show how to define schemas for consistent, typed responses.

#### Search Scraper with Schema (`searchscraper_tool_schema.py`)
**Purpose**: Extract product information with structured output.

**Schema Features**:
- Product name and description
- Feature lists with structured details
- Pricing information with multiple plans
- Reference URLs for verification

**Key Schema Classes**:
- `Feature`: Product feature details
- `PricingPlan`: Pricing tier information
- `ProductInfo`: Complete product information

#### Smart Scraper with Schema (`smartscraper_tool_schema.py`)
**Purpose**: Extract website information with structured output.

**Schema Features**:
- Website title and description
- URL extraction from page
- Support for both URL and HTML input

**Key Schema Classes**:
- `WebsiteInfo`: Complete website information structure

#### Smart Crawler with Schema (`smartcrawler_tool_schema.py`)
**Purpose**: Extract company information from multiple pages with structured output.

**Schema Features**:
- Company description
- Privacy policy content
- Terms of service content
- Multi-page content aggregation

**Key Schema Classes**:
- `CompanyInfo`: Company information structure

## Tool Parameters Reference

### SmartScraperTool
- `website_url`: Target website URL
- `user_prompt`: What information to extract
- `website_html`: (Optional) HTML content instead of URL
- `llm_output_schema`: (Optional) Pydantic model for structured output

### SearchScraperTool
- `user_prompt`: Search query and extraction instructions
- `llm_output_schema`: (Optional) Pydantic model for structured output

### SmartCrawlerTool
- `url`: Starting URL for crawling
- `prompt`: What information to extract
- `cache_website`: (Optional) Cache pages for efficiency
- `depth`: (Optional) Maximum crawling depth
- `max_pages`: (Optional) Maximum pages to crawl
- `same_domain_only`: (Optional) Restrict to same domain
- `llm_output_schema`: (Optional) Pydantic model for structured output

### GetCreditsTool
- No parameters required

### MarkdownifyTool
- `website_url`: Target website URL

## Best Practices

1. **Error Handling**: Always wrap tool calls in try-catch blocks for production use
2. **Rate Limiting**: Be mindful of API rate limits when making multiple requests
3. **Caching**: Use website caching for SmartCrawlerTool when processing multiple pages
4. **Structured Output**: Use Pydantic schemas for consistent, typed responses
5. **Logging**: Enable logging to debug and monitor tool performance

## Troubleshooting

- **Authentication Issues**: Ensure SGAI_API_KEY is properly set
- **Import Errors**: Install all required dependencies
- **Timeout Issues**: Increase timeout values for complex crawling operations
- **Rate Limiting**: Implement delays between requests if hitting rate limits

## Additional Resources

- [ScrapeGraph AI Documentation](https://docs.scrapegraphai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
