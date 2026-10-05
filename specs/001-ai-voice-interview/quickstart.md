# Quickstart Validation Guide

Follow these steps to run and validate the AI HR Interview Screening application.

## 1. Prerequisites
- Python 3.11+
- Google Gemini API Key (`GEMINI_API_KEY`)
- Google Chrome or a Chromium-based browser (to validate Web Speech API features)

## 2. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create your `.env` configuration:
```bash
cp .env.example .env
# Edit .env to set your GEMINI_API_KEY
```

## 3. Launch the Application
Start the FastAPI server:
```bash
python app/main.py
```
Or via uvicorn directly:
```bash
uvicorn app.main:app --reload --port 8000
```
Open your browser to: `http://localhost:8000`

---

## 4. End-to-End Validation Scenarios

### Scenario A: Normal Voice Interview Journey (Senior Level)
1. **Setup**: Enter Name: `Alex Rivera`, Role: `DevOps Engineer`, Level: `Senior Level`. Click **Start Interview**.
2. **First Question**: The browser will request microphone permission. Allow it. Observe status changes from `Connecting` to `AI Speaking` as the AI asks its first senior-level technical question.
3. **Voice Response**: Wait until AI finishes speaking. The status will transition to `Listening`. Speak a short technical answer into your microphone and click Finish / wait for silence.
4. **Processing & Next Question**: Status indicator briefly transitions to `Processing`, followed by `AI Speaking` with question 2 of 5.
5. **Completion**: Repeat for 5 questions. After answering question 5, the app transitions automatically to the **Results** screen displaying strengths, areas for improvement, and overall screening assessment.

### Scenario B: Dynamic Experience Level Tone Validation (Entry Level)
1. Start a new interview with Level: `Entry Level`.
2. Notice the initial and subsequent questions adopt a warm, introductory tone, focusing on basic concepts and learning willingness rather than complex architectural trade-offs.

### Scenario C: Fallback to Text Input (Microphone Denied)
1. Click **Start Interview** and deny microphone permissions when prompted.
2. The UI will show a friendly banner explaining microphone access was denied, and display a text area to allow typing answers.
3. Type an answer and submit. The interview continues normally across all 5 questions.
