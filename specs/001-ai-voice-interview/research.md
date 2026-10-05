# Phase 0: Research & Technical Validation

## Decision: Backend Language & Framework
- **Decision**: Python 3.11+ using FastAPI
- **Rationale**: Python is ideal for AI integration with Google ADK. FastAPI offers asynchronous capabilities required for non-blocking API routing and easy strict typing structures using Pydantic.
- **Alternatives considered**: Flask (acceptable, but lacks built-in async + Pydantic serialization natively).

## Decision: Agent Framework
- **Decision**: Google Agent Development Kit (Google ADK) / Gemini Models via Python SDK
- **Rationale**: Explicitly mandated by the user specifications as the core framework.
- **Alternatives considered**: Custom TypeScript/Node MCP (rejected as project-level instructions direct use of Python Google ADK). 

## Decision: Voice Interaction Implementation
- **Decision**: Browser Web Speech API (`SpeechRecognition` for STT, `SpeechSynthesis` for TTS)
- **Rationale**: Requires zero external API keys for voice, works client-side. Simplest architecture for an educational project, mitigating the need for real-time audio socket streaming to the backend. The backend just needs to receive text.
- **Alternatives considered**: Server-side integrations using OpenAI Whisper/TTS or Google Cloud Speech APIs (rejected for added complexity, cost, and explicit recommendation of Browser Web Speech APIs in spec).

## Decision: State Persistence
- **Decision**: In-memory Python `dict` grouped by a generated UUID.
- **Rationale**: Continues adherence to MVP constraints ("Do not introduce a database unless later requirements make persistence necessary").
- **Alternatives considered**: SQLite or Redis (rejected due to architectural constraints).