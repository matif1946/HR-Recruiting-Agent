# Feature Specification: AI Voice Interview Screening

**Feature Branch**: `001-ai-voice-interview`

**Created**: 2026-10-05

**Status**: Draft

**Input**: User description: "Build a web-based AI HR Interview Screening application that conducts interactive voice interviews with candidates."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Candidate Setup and Interview Initialization (Priority: P1)

Candidates must be able to input their personal details and experience level to initialize a customized AI interview session.

**Why this priority**: Required to initialize the interview and establish the fundamental dynamic context (experience level, role) for the AI agent.

**Independent Test**: Can be independently tested by entering candidate data on the setup screen and verifying data is passed to the interview initialization state without starting actual voice functionality.

**Acceptance Scenarios**:

1. **Given** a user is on the Candidate Setup screen, **When** they fill in their Name, Role, and select "Senior Level" and click Start, **Then** the application transitions to the Voice Interview screen with the correct level parameters set.
2. **Given** the user is on the Candidate Setup screen, **When** they attempt to start without entering all required fields, **Then** they are prompted to complete the missing information.

---

### User Story 2 - Voice-based Interview Interaction (Priority: P1)

Candidates must be able to engage in a back-and-forth voice conversation with the AI interviewer, where the AI's behavior adapts dynamically to the selected experience level.

**Why this priority**: This is the core functional requirement of the application, demonstrating voice interaction and dynamic instruction handling.

**Independent Test**: Can be tested by mocking the candidate setup and injecting voice inputs, verifying the AI responds with spoken text that varies in complexity based on the mocked experience level.

**Acceptance Scenarios**:

1. **Given** an interview is active for an "Entry Level" role, **When** the AI asks a question and the candidate responds via voice, **Then** the AI processes the answer and responds with an encouraging and fundamental follow-up question.
2. **Given** an interview is active for a "Senior Level" role, **When** the candidate answers a question, **Then** the AI responds with rigorous, challenging scenario-based questions.
3. **Given** the candidate is interacting via voice, **When** the system state changes between listening, processing, and AI speaking, **Then** the UI clearly displays the current visual status.

---

### User Story 3 - Text Fallback for Accessibility/Microphone Failure (Priority: P2)

Candidates must have a text-based fallback mechanism to continue the interview if they cannot use a microphone.

**Why this priority**: Ensures accessibility for all users and handles hardware failure gracefully, but the primary focus is voice.

**Independent Test**: Can be tested by denying microphone permissions and verifying the text input box appears and allows form submission that triggers the next AI question.

**Acceptance Scenarios**:

1. **Given** the candidate is on the Voice Interview screen, **When** microphone permissions are denied, **Then** the application displays a clear message and exposes a text input UI to continue the interview.
2. **Given** the candidate uses the text fallback, **When** they submit a text response, **Then** the AI processes it exactly as it would a voice response and issues the next question.

---

### User Story 4 - Interview Completion and Assessment (Priority: P2)

Candidates must receive a professional assessment summary summarizing their strengths and areas for improvement after answering 5 questions.

**Why this priority**: Closes the interview loop, providing demonstrable output of the AI's comprehension of the candidate's answers.

**Independent Test**: Can be tested by mocking 5 completed questions and answers and verifying the system generates and displays the summary payload correctly.

**Acceptance Scenarios**:

1. **Given** a candidate has just submitted an answer to the 5th question, **When** the AI completes processing, **Then** the system automatically ends the interview and transitions to the Results screen.
2. **Given** the Results screen is active, **When** it loads, **Then** it displays Candidate Name, Role, Level, Overall Summary, Strengths, Areas for Improvement, and an Overall Assessment.

### Edge Cases

- What happens if the browser does not support the Web Speech API / required voice APIs?
- How does the system handle an AI response timeout or failure during the "Processing" state?
- What happens if the candidate stops speaking completely for a prolonged period while the microphone is active?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST collect the candidate's Name, Role, and Experience Level (Entry, Mid, Senior) before starting the interview.
- **FR-002**: The system MUST adjust the AI interviewer's prompt instructions dynamically based on the selected Experience Level using a single underlying agent.
- **FR-003**: The system MUST request microphone permissions to capture the candidate's spoken responses.
- **FR-004**: The system MUST provide clear visual indicators for states: Setup, Connecting, AI Speaking, Listening, Candidate Speaking, Processing, Next Question, Error, and Interview Complete.
- **FR-005**: The system MUST convert the candidate's spoken voice to text internally to process the response.
- **FR-006**: The system MUST convert the AI's text responses to voice to speak to the candidate.
- **FR-007**: The system MUST provide a text-input fallback if the microphone is unavailable or permission is denied, without exposing internal errors.
- **FR-008**: The system MUST maintain conversation context across the sequence of questions, tracking previously asked questions and answers.
- **FR-009**: The system MUST enforce a limit of 5 questions per interview session.
- **FR-010**: The system MUST display an indication of progress (e.g., "Question 2 of 5").
- **FR-011**: The system MUST generate a final structured assessment upon completion containing Summary, Strengths, Areas for Improvement, and Overall Assessment.
- **FR-012**: The UI MUST prevent duplicate submissions during the "Processing" state.
- **FR-013**: The system MUST NOT expose internal API keys, system instructions, or debug information to the candidate interface.
- **FR-014**: The system MUST implement a voice integration using native Browser Web Speech APIs for both Speech-to-Text (capturing candidate voice) and Text-to-Speech (AI voice), minimizing external API dependencies.

### Key Entities

- **InterviewSession**: Tracks candidate details (Name, Role, Level), current state, progress (current question count / max questions), and the history of the conversation context.
- **Assessment**: Represents the final evaluation payload (Overall Summary, Strengths, Areas for Improvement, Overall Assessment).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A candidate can successfully navigate from the setup screen through a complete 5-question voice interview.
- **SC-002**: The interviewer accurately adapts its questioning style as validated by comparing a transcript of a Senior Level interview versus an Entry Level interview for the same role.
- **SC-003**: The visual state indicators accurately update to reflect the underlying state change during the audio interaction phases.
- **SC-004**: Accessing the assessment page reliably generates a structured response extracting candidate strengths and weaknesses from the conversation history.
- **SC-005**: Voice failure gracefully degrades to a text input interface without application crashes.

## Assumptions

- Uses modern browsers (Chrome/Edge/Safari/Firefox) supporting Web Audio APIs or standard HTML5 media APIs.
- Real-time voice processing will tolerate standard API latencies and doesn't require instantaneous sub-50ms reaction times.
- State will be managed primarily in memory/session for the duration of the interview (no persistent database required based on the specification).