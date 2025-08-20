import json

from pydantic import BaseModel, Field
from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import AgenticScraperTool

sgai_logger.set_logging(level="INFO")


# Define output schemas for different use cases
class UserProfileInfo(BaseModel):
    username: str = Field(description="The user's username")
    email: str = Field(description="The user's email address")
    dashboard_sections: list[str] = Field(description="Available dashboard sections")
    available_settings: list[str] = Field(description="Available user settings")


class ProductInfo(BaseModel):
    product_name: str = Field(description="The name of the product")
    price: str = Field(description="The price of the product")
    description: str = Field(description="Product description")
    availability: str = Field(description="Product availability status")
    rating: float = Field(description="Product rating out of 5")


class LoginResult(BaseModel):
    success: bool = Field(description="Whether login was successful")
    error_message: str = Field(description="Error message if login failed", default="")
    redirect_url: str = Field(description="URL to redirect to after login", default="")


# Initialize the tool with different schemas for different use cases
print("=== Example 1: User Profile Extraction with Schema ===")
tool_with_profile_schema = AgenticScraperTool(llm_output_schema=UserProfileInfo)

dashboard_url = "https://dashboard.example.com"
dashboard_steps = [
    "Navigate to user profile section",
    "Click on settings tab",
    "Wait for page to load",
]

try:
    result = tool_with_profile_schema.invoke(
        {
            "url": dashboard_url,
            "steps": dashboard_steps,
            "ai_extraction": True,
            "user_prompt": "Extract user profile information and available dashboard sections and settings",
            "use_session": True,
        }
    )
    print("User Profile Result:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50 + "\n")

print("=== Example 2: Product Information Extraction with Schema ===")
tool_with_product_schema = AgenticScraperTool(llm_output_schema=ProductInfo)

ecommerce_url = "https://shop.example.com"
search_steps = [
    "Type 'laptop' in search input box",
    "Click on search button",
    "Wait for results to load",
    "Click on first product",
]

try:
    result = tool_with_product_schema.invoke(
        {
            "url": ecommerce_url,
            "steps": search_steps,
            "ai_extraction": True,
            "user_prompt": "Extract product information including name, price, description, availability, and rating",
            "use_session": True,
        }
    )
    print("Product Info Result:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50 + "\n")

print("=== Example 3: Login Process with Schema ===")
tool_with_login_schema = AgenticScraperTool(llm_output_schema=LoginResult)

login_url = "https://example.com/login"
login_steps = [
    "Type 'user@example.com' in email input box",
    "Type 'password123' in password input box",
    "Click on login button",
    "Wait for response",
]

try:
    result = tool_with_login_schema.invoke(
        {
            "url": login_url,
            "steps": login_steps,
            "ai_extraction": True,
            "user_prompt": "Determine if login was successful and extract any error messages or redirect URLs",
            "use_session": True,
        }
    )
    print("Login Result:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50 + "\n")

# Example 4: Using dictionary schema instead of Pydantic model
print("=== Example 4: Dictionary Schema ===")
tool_with_dict_schema = AgenticScraperTool()

# Define schema as a dictionary
news_schema = {
    "news_article": {
        "type": "object",
        "properties": {
            "headline": {"type": "string"},
            "author": {"type": "string"},
            "publish_date": {"type": "string"},
            "content_summary": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
    }
}

news_url = "https://news.example.com"
news_steps = [
    "Navigate to latest news section",
    "Click on first article",
    "Wait for page to load",
]

try:
    result = tool_with_dict_schema.invoke(
        {
            "url": news_url,
            "steps": news_steps,
            "ai_extraction": True,
            "user_prompt": "Extract article headline, author, publish date, content summary, and tags",
            "output_schema": news_schema,
            "use_session": True,
        }
    )
    print("News Article Result:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
