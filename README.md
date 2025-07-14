# 🕷️🦜 langchain-scrapegraph

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Support](https://img.shields.io/pypi/pyversions/langchain-scrapegraph.svg)](https://pypi.org/project/langchain-scrapegraph/)
[![Documentation](https://img.shields.io/badge/Documentation-Latest-green)](https://docs.scrapegraphai.com/integrations/langchain)

Supercharge your LangChain agents with AI-powered web scraping capabilities. LangChain-ScrapeGraph provides a seamless integration between [LangChain](https://github.com/langchain-ai/langchain) and [ScrapeGraph AI](https://scrapegraphai.com), enabling your agents to extract structured data from websites using natural language.

## 🔗 ScrapeGraph API & SDKs
If you are looking for a quick solution to integrate ScrapeGraph in your system, check out our powerful API [here!](https://dashboard.scrapegraphai.com/login)

We offer SDKs in both Python and Node.js, making it easy to integrate into your projects. Check them out below:

| SDK       | Language | GitHub Link                                                                 |
|-----------|----------|-----------------------------------------------------------------------------|
| Python SDK | Python   | [scrapegraph-py](https://github.com/ScrapeGraphAI/scrapegraph-sdk/tree/main/scrapegraph-py) |
| Node.js SDK | Node.js  | [scrapegraph-js](https://github.com/ScrapeGraphAI/scrapegraph-sdk/tree/main/scrapegraph-js) |

## 📦 Installation

```bash
pip install langchain-scrapegraph
```

## 🛠️ Available Tools

### 📝 MarkdownifyTool
Convert any webpage into clean, formatted markdown.

```python
from langchain_scrapegraph.tools import MarkdownifyTool

tool = MarkdownifyTool()
markdown = tool.invoke({"website_url": "https://example.com"})

print(markdown)
```

### 🔍 SmartscraperTool
Extract structured data from any webpage using natural language prompts.

```python
from langchain_scrapegraph.tools import SmartScraperTool

# Initialize the tool (uses SGAI_API_KEY from environment)
tool = SmartscraperTool()

# Extract information using natural language
result = tool.invoke({
    "website_url": "https://www.example.com",
    "user_prompt": "Extract the main heading and first paragraph"
})

print(result)
```

### 🌐 SearchscraperTool
Search and extract structured information from the web using natural language prompts.

```python
from langchain_scrapegraph.tools import SearchScraperTool

# Initialize the tool (uses SGAI_API_KEY from environment)
tool = SearchScraperTool()

# Search and extract information using natural language
result = tool.invoke({
    "user_prompt": "What are the key features and pricing of ChatGPT Plus?"
})

print(result)
# {
#     "product": {
#         "name": "ChatGPT Plus",
#         "description": "Premium version of ChatGPT..."
#     },
#     "features": [...],
#     "pricing": {...},
#     "reference_urls": [
#         "https://openai.com/chatgpt",
#         ...
#     ]
# }
```

<details>
<summary>🔍 Using Output Schemas with SearchscraperTool</summary>

You can define the structure of the output using Pydantic models:

```python
from typing import List, Dict
from pydantic import BaseModel, Field
from langchain_scrapegraph.tools import SearchScraperTool

class ProductInfo(BaseModel):
    name: str = Field(description="Product name")
    features: List[str] = Field(description="List of product features")
    pricing: Dict[str, Any] = Field(description="Pricing information")
    reference_urls: List[str] = Field(description="Source URLs for the information")

# Initialize with schema
tool = SearchScraperTool(llm_output_schema=ProductInfo)

# The output will conform to the ProductInfo schema
result = tool.invoke({
    "user_prompt": "What are the key features and pricing of ChatGPT Plus?"
})

print(result)
# {
#     "name": "ChatGPT Plus",
#     "features": [
#         "GPT-4 access",
#         "Faster response speed",
#         ...
#     ],
#     "pricing": {
#         "amount": 20,
#         "currency": "USD",
#         "period": "monthly"
#     },
#     "reference_urls": [
#         "https://openai.com/chatgpt",
#         ...
#     ]
# }
```
</details>

## 🌟 Key Features

- 🐦 **LangChain Integration**: Seamlessly works with LangChain agents and chains
- 🔍 **AI-Powered Extraction**: Use natural language to describe what data to extract
- 📊 **Structured Output**: Get clean, structured data ready for your agents
- 🔄 **Flexible Tools**: Choose from multiple specialized scraping tools
- ⚡ **Async Support**: Built-in support for async operations

## 💡 Use Cases

- 📖 **Research Agents**: Create agents that gather and analyze web data
- 📊 **Data Collection**: Automate structured data extraction from websites
- 📝 **Content Processing**: Convert web content into markdown for further processing
- 🔍 **Information Extraction**: Extract specific data points using natural language

## 🤖 Example Agent

```python
from langchain.agents import initialize_agent, AgentType
from langchain_scrapegraph.tools import SmartScraperTool
from langchain_openai import ChatOpenAI

# Initialize tools
tools = [
    SmartScraperTool(),
]

# Create an agent
agent = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use the agent
response = agent.run("""
    Visit example.com, make a summary of the content and extract the main heading and first paragraph
""")
```

## ⚙️ Configuration

Set your ScrapeGraph API key in your environment:
```bash
export SGAI_API_KEY="your-api-key-here"
```

Or set it programmatically:
```python
import os
os.environ["SGAI_API_KEY"] = "your-api-key-here"
```

## 📚 Documentation

- [API Documentation](https://scrapegraphai.com/docs)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)
- [Examples](examples/)

## 💬 Support & Feedback

- 📧 Email: support@scrapegraphai.com
- 💻 GitHub Issues: [Create an issue](https://github.com/ScrapeGraphAI/langchain-scrapegraph/issues)
- 🌟 Feature Requests: [Request a feature](https://github.com/ScrapeGraphAI/langchain-scrapegraph/issues/new)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project is built on top of:
- [LangChain](https://github.com/langchain-ai/langchain)
- [ScrapeGraph AI](https://scrapegraphai.com)

---

Made with ❤️ by [ScrapeGraph AI](https://scrapegraphai.com)
