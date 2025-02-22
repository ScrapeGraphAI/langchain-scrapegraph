from typing import Dict, List

from pydantic import BaseModel, Field
from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import SearchScraperTool


class Feature(BaseModel):
    name: str = Field(description="Name of the feature")
    description: str = Field(description="Description of the feature")


class PricingPlan(BaseModel):
    name: str = Field(description="Name of the pricing plan")
    price: Dict[str, str] = Field(
        description="Price details including amount, currency, and period"
    )
    features: List[str] = Field(description="List of features included in the plan")


class ProductInfo(BaseModel):
    name: str = Field(description="Name of the product")
    description: str = Field(description="Description of the product")
    features: List[Feature] = Field(description="List of product features")
    pricing: Dict[str, List[PricingPlan]] = Field(description="Pricing information")
    reference_urls: List[str] = Field(description="Source URLs for the information")


sgai_logger.set_logging(level="INFO")

# Initialize with Pydantic model class
tool = SearchScraperTool(llm_output_schema=ProductInfo)

# Example prompt
user_prompt = "What are the key features and pricing of ChatGPT Plus?"

# Use the tool - output will conform to ProductInfo schema
result = tool.invoke({"user_prompt": user_prompt})

print("\nResult:", result)
