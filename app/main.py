import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# Load environment variables
load_dotenv()

app = FastAPI(title="AI HR Interview Screening API")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "HR Interview Screening Agent API"}


def verify_adk_agent():
    """
    Run the smallest possible ADK agent test to verify connectivity:
    Application -> Google ADK -> Gemini -> Response
    """
    print("Starting minimal ADK agent test...")
    api_key = os.getenv("GEMINI_API_KEY")

    if not HAS_GENAI:
        print("Error: google-genai library is not installed.")
        return False

    if not api_key or api_key == "your_gemini_api_key_here":
        print("Warning: GEMINI_API_KEY is not configured in .env.")
        print("Skipping actual Gemini API call.")
        return True

    try:
        # Initialize Google ADK / GenAI Client
        client = genai.Client(api_key=api_key)

        # Create a simple agent/chat session
        chat = client.chats.create(model="gemini-2.5-flash")

        print("Application -> Google ADK -> Gemini...")
        response = chat.send_message("Reply 'OK' if you can receive this message.")

        print("Response received:")
        print(response.text)
        return True
    except Exception as e:
        print(f"Error communicating with Gemini via Google ADK: {e}")
        return False


if __name__ == "__main__":
    success = verify_adk_agent()
    print("Setup Verification:", "PASSED" if success else "FAILED")

    # You can run the server via: uvicorn app.main:app --reload
