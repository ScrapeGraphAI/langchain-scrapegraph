from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import LocalScraperTool

sgai_logger.set_logging(level="INFO")

# Will automatically get SGAI_API_KEY from environment
tool = LocalScraperTool()

# Example website and prompt
html_content = """
<html>
    <body>
        <h1>Company Name</h1>
        <p>We are a technology company focused on AI solutions.</p>
        <div class="contact">
            <p>Email: contact@example.com</p>
            <p>Phone: (555) 123-4567</p>
        </div>
    </body>
</html>
"""
user_prompt = "Make a summary of the webpage and extract the email and phone number"

# Use the tool
result = tool.invoke({"website_html": html_content, "user_prompt": user_prompt})

print(result)
