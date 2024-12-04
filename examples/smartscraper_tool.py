from langchain_scrapegraph.tools import SmartscraperTool

# Will automatically get SGAI_API_KEY from environment, or set it manually
tool = SmartscraperTool()

# Example website and prompt
website_url = "https://www.example.com"
user_prompt = "Extract the main heading and first paragraph from this webpage"

# Use the tool synchronously
result = tool.run({"user_prompt": user_prompt, "website_url": website_url})

print("\nExtraction Results:")
print(f"Main Heading: {result['main_heading']}")
print(f"First Paragraph: {result['first_paragraph']}")
