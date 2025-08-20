import json

from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import AgenticScraperTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = AgenticScraperTool()

# Example 1: Basic usage with form filling and navigation
print("=== Example 1: Basic Form Filling ===")
url = "https://example.com/login"
steps = [
    "Type 'user@example.com' in email input box",
    "Type 'password123' in password input box",
    "Click on login button",
]

try:
    result = tool.invoke({"url": url, "steps": steps, "use_session": True})
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50 + "\n")

# Example 2: With AI extraction and structured output
print("=== Example 2: AI Extraction with Schema ===")
dashboard_url = "https://dashboard.example.com"
dashboard_steps = [
    "Navigate to user profile section",
    "Click on settings tab",
    "Wait for page to load",
]

# Define the output schema for structured data
output_schema = {
    "user_info": {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "email": {"type": "string"},
            "dashboard_sections": {"type": "array", "items": {"type": "string"}},
            "available_settings": {"type": "array", "items": {"type": "string"}},
        },
    }
}

try:
    result = tool.invoke(
        {
            "url": dashboard_url,
            "steps": dashboard_steps,
            "ai_extraction": True,
            "user_prompt": "Extract user profile information and available dashboard sections and settings",
            "output_schema": output_schema,
            "use_session": True,
        }
    )
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50 + "\n")

# Example 3: E-commerce product search
print("=== Example 3: E-commerce Product Search ===")
ecommerce_url = "https://shop.example.com"
search_steps = [
    "Type 'laptop' in search input box",
    "Click on search button",
    "Wait for results to load",
    "Click on first product",
]

search_schema = {
    "product_info": {
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "price": {"type": "string"},
            "description": {"type": "string"},
            "availability": {"type": "string"},
        },
    }
}

try:
    result = tool.invoke(
        {
            "url": ecommerce_url,
            "steps": search_steps,
            "ai_extraction": True,
            "user_prompt": "Extract product information including name, price, description, and availability",
            "output_schema": search_schema,
            "use_session": True,
        }
    )
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
