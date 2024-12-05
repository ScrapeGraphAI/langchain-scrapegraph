"""
Remember to install the additional dependencies for this example to work:
pip install langchain-openai langchain
"""

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from langchain_scrapegraph.tools import (
    GetCreditsTool,
    LocalScraperTool,
    SmartScraperTool,
)

load_dotenv()

# Initialize the tools
tools = [
    SmartScraperTool(),
    LocalScraperTool(),
    GetCreditsTool(),
]

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a helpful AI assistant that can analyze websites and extract information. "
                "You have access to tools that can help you scrape and process web content. "
                "Always explain what you're doing before using a tool."
            )
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Initialize the LLM
llm = ChatOpenAI(temperature=0)

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Create the executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
query = """Extract the main products from https://www.scrapegraphai.com/"""

print("\nQuery:", query, "\n")
response = agent_executor.invoke({"input": query})
print("\nFinal Response:", response["output"])
