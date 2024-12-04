from langchain_scrapegraph.tools import SubmitFeedbackTool

# Will automatically get SGAI_API_KEY from environment, or set it manually
tool = SubmitFeedbackTool()
feedback = tool.run(
    {
        "request_id": "5c7be764-2406-4ce0-b346-88f8825e6cb3",
        "rating": 5,
        "feedback_text": "Great result!",
    }
)

print("\nFeedback Submission Result:")
print(f"Feedback ID: {feedback['feedback_id']}")
print(f"Message: {feedback['message']}")
print(f"Timestamp: {feedback['feedback_timestamp']}")
