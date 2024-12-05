# 🕷️🦜 langchain-scrapegraph

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Support](https://img.shields.io/pypi/pyversions/langchain-scrapegraph.svg)](https://pypi.org/project/langchain-scrapegraph/)
[![Documentation](https://img.shields.io/badge/Documentation-Latest-green)](https://scrapegraphai.com/docs)

Supercharge your LangChain agents with AI-powered web scraping capabilities. LangChain-ScrapeGraph provides a seamless integration between [LangChain](https://github.com/langchain-ai/langchain) and [ScrapeGraph AI](https://scrapegraphai.com), enabling your agents to extract structured data from websites using natural language.

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
from langchain_scrapegraph.tools import SmartscraperTool

# Initialize the tool (uses SGAI_API_KEY from environment)
tool = SmartscraperTool()

# Extract information using natural language
result = tool.invoke({
    "website_url": "https://www.example.com",
    "user_prompt": "Extract the main heading and first paragraph"
})

print(result)
```

### 💻 LocalscraperTool
Extract information from HTML content using AI.

```python
from langchain_scrapegraph.tools import LocalscraperTool

tool = LocalscraperTool()
result = tool.invoke({
    "user_prompt": "Extract all contact information",
    "website_html": "<html>...</html>"
})

print(result)
```

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
from langchain_scrapegraph.tools import SmartscraperTool
from langchain_openai import ChatOpenAI

# Initialize tools
tools = [
    SmartscraperTool(),
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
