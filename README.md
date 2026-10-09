# AI HR Interview Screening

A voice-activated, Gemini-powered HR recruiter agent. 

## About
This MVP application acts as a screening interviewer. The user supplies their name, job role, and target experience level (Entry, Mid, Senior). The `google-genai` agent backend issues conversational screening questions, and the frontend connects browser-native SpeechRecognition and SpeechSynthesis functionality for hands-free voice interviews with robust text fallback operations.

## Architecture Structure
**Frontend (Web Speech API)** 👉 **FastAPI Backend (`app/api`)** 👉 **Google ADK (`app/agent`)** 👉 **Gemini (Flash)**

The Frontend utilizes `window.SpeechRecognition` and `window.speechSynthesis` natively to bridge microphone and speaker access without heavy websocket configurations. It sends standardized JSON textual API requests via `fetch()` to FastAPI endpoints `/api/interviews`.

The AI (`InterviewerAgent`) reads from In-Memory `InterviewService` tracking, constructs targeted prompts matching local history, issues instructions based on `ExperienceLevel`, calls the `gemini-2.5-flash` model, and delivers a subsequent localized string question backward to the user securely.

## Dynamic Instructions
Instruction modifiers are mapped dynamically from `ExperienceLevel`:
1. **Entry**: Focuses on potential, encouragement, and fundamental validation.
2. **Mid**: Evaluates practical trade-offs, autonomous system design inputs, and situational history.
3. **Senior**: Rigorous analysis, architectural ownership, scaling strategies, and deep organizational trade-offs.

## Setting Up
1. `python -m venv .venv` and `source .venv/Scripts/activate`
2. `pip install -r requirements.txt`
3. Export `GEMINI_API_KEY=your_key_here` (or via `.env` file).
4. Run server: `uvicorn app.main:app --reload`
5. Open browser at `http://127.0.0.1:8000`.

## Testing
Comprehensive testing utilizes Pytest covering both End-to-End API fallback strategies alongside isolated localized instruction generation constraints.
`pytest tests/`
