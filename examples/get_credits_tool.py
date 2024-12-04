from langchain_scrapegraph.tools import GetCreditsTool

# Will automatically get SGAI_API_KEY from environment, or set it manually
tool = GetCreditsTool()
credits = tool.run()

print("\nCredits Information:")
print(f"Remaining Credits: {credits['remaining_credits']}")
print(f"Total Credits Used: {credits['total_credits_used']}")
