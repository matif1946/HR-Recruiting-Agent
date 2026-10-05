# Implementation Plan: AI Voice Interview

**Branch**: `001-ai-voice-interview` | **Date**: 2026-10-06 | **Spec**: [specs/001-ai-voice-interview/spec.md](spec.md)

**Input**: Feature specification from `/specs/001-ai-voice-interview/spec.md`

## Summary

Build an AI HR Interview Screening application for candidates, leveraging Python and Google ADK to drive a Gemini-powered interviewer. The agent's instructions update dynamically per the candidate's selected experience level (Entry, Mid, Senior) while using Browser Web Speech APIs for seamless voice-based interactions.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), HTML/Vanilla JS + CSS (Frontend)

**Primary Dependencies**:
- Python backend: `google-genai` (Google ADK for Python), `fastapi`, `uvicorn`, `python-dotenv`
- Frontend: Native browser `SpeechRecognition` and `speechSynthesis` APIs (No external dependencies)

**Storage**: In-memory state only (no database per spec).

**Testing**: `pytest`, `pytest-asyncio`

**Target Platform**: Web browsers (Chrome-optimized for Web Speech API), local Python server environment.

**Project Type**: Web Application (Backend API + Static Frontend Web interface)

**Performance Goals**: AI/Agent voice preparation API responses should not significantly block the standard flow, status indicators will reflect `PROCESSING`. 

**Constraints**: In-memory data store means all state is lost on restart. Voice STT/TTS requires specific modern browser support.

**Scale/Scope**: MVPs - 1 Interview Session (5 questions max per candidate).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **PASS**: Python and Google ADK are used as the primary framework (Rule II).
- **PASS**: Single agent logic, dynamically instructed (Rule I).
- **PASS**: Small scope, UI first class requirement (Rule IV, VIII).
- **PASS**: Minimal UI, no raw exception dumps (Rule VII, IX).

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-voice-interview/
├── plan.md              # This file
├── research.md          
├── data-model.md        
├── quickstart.md        
├── contracts/           
└── tasks.md             
```

### Source Code (repository root)

```text
app/
├── agent/
│   ├── interviewer.py    # Google ADK agent setup
│   ├── instructions.py   # Dynamic instruction builders
│   └── assessment.py     # Final assessment generation logic
├── api/
│   └── interviews.py     # FastAPI router endpoints
├── models/
│   └── interview.py      # Pydantic models for State
├── services/
│   ├── interview_service.py # Core business logic connecting logic and agent
│   └── voice_service.py     # Helper definitions for separating voice processing config
├── static/               # Frontend assets
│   ├── index.html        # SPA implementation
│   ├── app.js            # Frontend logic (Voice states, API calls)
│   └── style.css         # HR styling
└── main.py               # Application entrypoint

tests/
├── test_instructions.py
├── test_interview.py
└── test_api.py
```

**Structure Decision**: We will use a Python application using FastAPI to serve static components (`app/static`). This matches the prompt's defined layers and folder structure precisely.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |