"""Monitor Tool Example - LangChain Tool (v2 API)

Replaces the old Scheduled Jobs tools. Uses the monitor namespace.
"""

from langchain_scrapegraph.tools import MonitorCreateTool, MonitorListTool

# Initialize tools
create_tool = MonitorCreateTool()
list_tool = MonitorListTool()

# Create a monitor
result = create_tool.invoke(
    {
        "name": "Price Monitor",
        "url": "https://example.com/products",
        "prompt": "Extract current product prices",
        "cron": "0 9 * * *",  # Daily at 9 AM
    }
)
print("Monitor created:", result)

# List all monitors
monitors = list_tool.invoke({})
print("All monitors:", monitors)
