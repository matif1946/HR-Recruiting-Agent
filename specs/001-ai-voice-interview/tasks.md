---
description: "Task list for AI Voice Interview Screening feature implementation"
---

# Tasks: AI Voice Interview Screening

**Input**: Design documents from `/specs/001-ai-voice-interview/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base configuration

- [x] T001 Initialize project structure: Create directory structure (`app/agent`, `app/api`, `app/models`, `app/services`, `app/static`, `tests`) and base placeholders
- [x] T002 Configure Python environment: Create `requirements.txt` with dependencies (`google-genai`, `fastapi`, `uvicorn`, `python-dotenv`, `pytest`, `pytest-asyncio`)
- [x] T003 Configure environment variables: Create `.env.example` and establish configuration management with `GEMINI_API_KEY`
- [x] T004 Configure Google ADK: Install/configure `google-genai` and verify minimal ADK agent runs successfully in `app/main.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain models, instruction engine, and interviewer agent base that MUST be complete before user stories

- [x] T005 [P] Create interview state model: Implement Pydantic models with `ExperienceLevel`, `VoiceState`, `CandidateInfo`, and `InterviewState` in `app/models/interview.py`
- [x] T006 [P] Add input validation: Validate Name/Role/Experience rejecting incomplete data in `app/models/interview.py`
- [x] T007 Create interview lifecycle service: Implement in-memory state storage, session lookup, and question progression in `app/services/interview_service.py`
- [x] T008 [P] Create dynamic instruction builder: Implement `build_interview_instructions` component in `app/agent/instructions.py`
- [x] T009 [P] Implement entry-level instructions: Create warm, encouraging fundamental dynamic instructions in `app/agent/instructions.py`
- [x] T010 [P] Implement mid-level instructions: Create professional scenario-based dynamic instructions in `app/agent/instructions.py`
- [x] T011 [P] Implement senior-level instructions: Create rigorous, architectural trade-off dynamic instructions in `app/agent/instructions.py`
- [x] T012 Create Google ADK interviewer agent: Implement primary single interviewer agent instance in `app/agent/interviewer.py`
- [x] T013 Connect dynamic instructions to agent: Pass runtime instructions based on interview state in `app/agent/interviewer.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Candidate Setup and Interview Initialization (Priority: P1)

**Goal**: Candidates input details to start customized interview session.

**Independent Test**: `POST /api/interviews` executes successfully with candidate data, initializing the ADK agent with the first generated question.

### Implementation for User Story 1

- [x] T014 [US1] Implement first-question generation: Generate initial question according to role and level in `app/agent/interviewer.py`
- [x] T015 [US1] Create interview API: Implement endpoint `POST /api/interviews` returning session ID and initial question in `app/api/interviews.py`
- [x] T016 [P] [US1] Create application layout: Build clean, responsive application skeleton in `app/static/index.html` and `app/static/style.css`
- [x] T017 [US1] Build candidate setup screen: Implement Name, Job Role, Experience Level selection, and Start Interview button in `app/static/index.html` and `app/static/app.js`
- [x] T018 [US1] Add loading and error states for setup: Handle loading indicators and invalid input banners in `app/static/app.js` and `app/static/style.css`

**Checkpoint**: At this point, User Story 1 generates a session ID and initial AI question successfully.

---

## Phase 4: User Story 2 - Voice-based Interview Interaction (Priority: P1)

**Goal**: Engage in back-and-forth voice interactions adapted to candidate experience level.

**Independent Test**: AI generates subsequent questions based on answers without repeating, utilizing speech-to-text input and voice synthesis playback.

### Implementation for User Story 2

- [x] T019 [P] [US2] Implement context-aware next-question generation: Generate subsequent questions using previous responses in `app/agent/interviewer.py`
- [x] T020 [P] [US2] Prevent unnecessary repetition: Ensure interviewer does not repeat previous questions in `app/agent/interviewer.py`
- [x] T021 [US2] Create response API: Implement endpoint for submitting candidate responses at `POST /api/interviews/{id}/response` in `app/api/interviews.py`
- [x] T022 [US2] Build interview screen: Implement candidate info header, progress indicator, AI question display, and voice interaction container in `app/static/index.html` and `app/static/app.js`
- [x] T023 [US2] Implement browser microphone access: Request Web Speech mic permissions and handle denial gracefully in `app/static/app.js`
- [x] T024 [US2] Implement candidate voice capture and silence handling: Capture spoken response via SpeechRecognition and detect prolonged silence timeouts gracefully in `app/static/app.js`
- [x] T025 [US2] Implement speech processing: Convert candidate voice response to text string for API submission in `app/static/app.js`
- [x] T026 [US2] Connect voice response to interview agent: Send processed candidate response through interview workflow in `app/static/app.js`
- [x] T027 [US2] Implement AI voice output: Play interviewer questions using SpeechSynthesis in `app/static/app.js`
- [x] T028 [US2] Implement voice interaction states: Visually reflect IDLE, LISTENING, PROCESSING, AI_SPEAKING, ERROR, and COMPLETED in `app/static/app.js` and `app/static/style.css`
- [x] T029 [US2] Add microphone/interview controls: Implement start/stop speaking, retry mic, and end interview controls in `app/static/index.html` and `app/static/app.js`
- [x] T030 [US2] Prevent conflicting voice actions: Disable duplicate recording actions while AI is speaking or processing in `app/static/app.js`

**Checkpoint**: Working continuous back-and-forth voice interview iteration via Browser Web Speech APIs.

---

## Phase 5: User Story 3 - Voice Fallback & Error Resilience (Priority: P2)

**Goal**: Seamlessly support manual text fallback when microphone interaction fails or is denied.

**Independent Test**: Declining mic permission immediately presents fallback textarea allowing interview progression without state loss.

### Implementation for User Story 3

- [x] T031 [US3] Implement microphone error handling and capability checks: Explicitly check for Web Speech API browser support (`window.SpeechRecognition`), and gracefully handle permission denied and device unavailable errors in `app/static/app.js`
- [x] T032 [US3] Implement text-answer fallback: Provide accessible text input area submitting to the same interview API in `app/static/index.html` and `app/static/app.js`
- [x] T033 [US3] Preserve interview state during voice failures: Ensure microphone errors do not restart or corrupt current session state in `app/static/app.js`

---

## Phase 6: User Story 4 - Interview Completion & Assessment (Priority: P2)

**Goal**: Complete 5 questions and generate structured screening assessment.

**Independent Test**: Answering question 5 completes interview and outputs structured assessment with summary, strengths, and improvements.

### Implementation for User Story 4

- [x] T034 [US4] Implement five-question interview flow: Stop question progression after 5 answered questions in `app/services/interview_service.py`
- [x] T035 [US4] Implement final assessment generation: Generate overall summary, key strengths, and improvement areas in `app/agent/assessment.py`
- [x] T036 [US4] Ensure assessment is screening assistance: Include explicit disclaimer that report is an aid and not a hiring decision in `app/agent/assessment.py`
- [x] T037 [P] [US4] Create interview-state API: Implement endpoint for retrieving current state `GET /api/interviews/{id}` in `app/api/interviews.py`
- [x] T038 [P] [US4] Create interview completion API: Implement endpoint for terminating interview early `POST /api/interviews/{id}/end` in `app/api/interviews.py`
- [x] T039 [US4] Build results screen: Render interview completion message, candidate summary, strengths, areas for improvement, assessment, and restart button in `app/static/index.html` and `app/static/app.js`

**Checkpoint**: Happy path completed strictly through to Assessment report rendering.

---

## Phase 7: Polish, Testing & Documentation

**Purpose**: UI/UX refinement, comprehensive testing, error hardening, responsive styling, and project documentation

### UI/UX Refinement
- [x] T040 Add API error handling: Implement global exception handlers preventing credential/stack trace leaks in `app/main.py`
- [x] T041 Refine professional visual design: Polish typography, spacing, visual hierarchy, and restrained color palette in `app/static/style.css`
- [x] T042 Improve voice feedback: Enhance visual indicators for AI speaking, candidate listening, candidate speaking, and processing states in `app/static/style.css` and `app/static/app.js`
- [x] T043 Add interview progress: Display "Question X of 5" status prominently in `app/static/index.html` and `app/static/app.js`
- [x] T044 Verify mobile usability: Ensure setup, interview controls, voice interactions, and results screens are responsive and accessible on mobile in `app/static/style.css`

### Comprehensive Testing
- [x] T045 [P] Test candidate validation: Verify valid and invalid candidate setup data in `tests/test_interview.py`
- [x] T046 [P] Test dynamic instruction behavior: Verify all three experience levels produce appropriate runtime instructions in `tests/test_instructions.py`
- [x] T047 [P] Test interview progression: Verify questions and answers progress correctly in `tests/test_interview.py`
- [x] T048 [P] Test five-question completion: Verify the interview completes after five questions in `tests/test_interview.py`
- [x] T049 [P] Test final assessment: Verify the final assessment contains all required sections in `tests/test_interview.py`
- [x] T050 [P] Test API error handling: Verify failures produce user-friendly errors in `tests/test_api.py`
- [x] T051 [P] Test voice failure scenarios: Test microphone denied, unavailable, and processing failures gracefully recover (via mocked backend/UI tests) in `tests/test_api.py`
- [x] T052 [P] Test text fallback: Verify that text fallback continues the same interview correctly in `tests/test_api.py`
- [x] T053 [P] Test complete end-to-end interview: Test full backend flow from Setup -> Start -> Next question -> Assessment in `tests/test_api.py`

### Documentation & Verification
- [x] T054 Create README: Document project purpose, features, ADK usage, flow, setup, and testing in `README.md`
- [x] T055 Document architecture: Include simple Frontend -> API -> ADK -> Gemini architecture diagram/explanation in `README.md`
- [x] T056 Document dynamic instructions: Explain entry/mid/senior level modification of runtime instructions in `README.md`
- [x] T057 Document voice architecture: Explain Web Speech API to Backend AI response flow in `README.md`
- [x] T058 Run complete MVP verification: Execute manual end-to-end MVP validation according to steps defined in `quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all User Stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion.
- **User Story 3 (Phase 5)**: Can proceed alongside or immediately following User Story 2.
- **User Story 4 (Phase 6)**: Depends on User Story 2 completion.
- **Phase 7 (Polish/Tests/Docs)**: Depends on all user stories being broadly complete.

### Parallel Execution Opportunities

- T005, T006, T008, T009, T010, T011 can be implemented concurrently during Phase 2.
- T016 (Layout skeleton) can be authored in parallel with backend endpoints.
- T019, T020 (Agent question generation logic) can be refined in parallel with frontend voice listeners.
- T037, T038 (Auxiliary API endpoints) can be built in parallel with assessment agent logic.
- T045-T053 (Tests) can all be run in parallel once the implementations exist.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)
1. Complete Setup (Phase 1) and Foundational (Phase 2).
2. Implement Candidate Setup and Interview Initialization (User Story 1).
3. Implement Voice Interaction and Next-Question generation (User Story 2).
4. Validate basic voice interview loop locally.
5. Add Text Fallback (User Story 3) and 5-Question Completion Assessment (User Story 4).
6. Implement Polish, complete Test suite, and finalize documentation (Phase 7).

### Task: Handle prolonged candidate silence

Implement silence detection during the LISTENING state.

If the candidate does not speak for a configurable period:

1. Stop the current listening attempt.
2. Inform the candidate that no response was detected.
3. Prompt the candidate to speak again.
4. Allow the candidate to retry.

If the candidate repeatedly remains silent after the configured number of
attempts, provide the option to:

- Retry the voice response
- Switch to text input
- End the interview

The silence timeout must not destroy the existing interview state.

### Task: Detect browser voice capability

Before starting the voice interview, detect whether the browser supports
the required Web Speech API functionality.

If SpeechRecognition is unavailable:

1. Do not attempt to start voice recording.
2. Display a clear message explaining that voice input is unavailable.
3. Automatically offer the text-answer fallback.
4. Continue using the same interview state and agent logic.

The application must not crash because the browser does not support the
required voice functionality.