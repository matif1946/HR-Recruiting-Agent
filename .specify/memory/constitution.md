<!-- Sync Impact Report
Version Change: New implementation
Follow-up TODOs: None
-->
Project: AI HR Interview Screening Agent

This project follows Spec-Driven Development (SDD) and is governed by the
following principles.

## Core Principles

### I. Dynamic Interview Intelligence

The system MUST use dynamic instructions as the core Agentic AI concept.

The interviewer's behavior MUST change at runtime based on the candidate's
selected experience level or role level.

At minimum, the system MUST support:
- Entry-level candidates
- Mid-level candidates
- Senior-level candidates

Entry-level interviews SHOULD use a warm, encouraging, beginner-friendly
style with fundamental questions.

Mid-level interviews SHOULD use moderately challenging technical and
scenario-based questions.

Senior-level interviews MUST use more rigorous technical, analytical,
scenario-based, and role-relevant questions.

The system MUST NOT create separate hardcoded agents for each experience
level. A common interviewer agent MUST receive dynamically constructed
instructions appropriate to the selected level.

### II. Google ADK First

Google Agent Development Kit (ADK) MUST be the primary agent framework.

Python MUST be used as the primary programming language for the agent
implementation.

The project MUST NOT require a custom MCP framework for its core agent
logic.

Agent behavior, instruction management, execution, and agent-related
functionality MUST use Google ADK.

The architecture SHOULD remain simple and understandable for an
educational Agentic AI project.

MCP MAY be introduced later only if a clearly defined project requirement
requires external tools or context integration. It MUST NOT replace Google
ADK as the primary agent framework.

### III. Spec-Driven Development

All significant development MUST follow the Spec-Driven Development
workflow.

Requirements MUST be defined before implementation.

The project MUST maintain clear separation between:
- What the system should do
- How the system will be implemented
- The individual implementation tasks

The project SHOULD follow the Spec Kit workflow:

constitution → specify → clarify → plan → tasks → analyze → implement

Changes to requirements MUST be reflected in the appropriate specification
before implementation whenever practical.

### IV. User Interface First-Class Requirement

The application MUST provide a usable graphical web interface.

The UI MUST allow a recruiter or interviewer to:
- Start an interview
- Enter candidate information
- Select the candidate's experience level
- Start the AI interview
- View AI-generated questions
- Enter candidate answers
- Continue the interview
- Complete the interview
- View the interview result or summary

The interface MUST clearly communicate the current interview state.

The UI SHOULD be clean, professional, responsive, and appropriate for an
HR/recruitment application.

The UI MUST NOT expose internal prompts, hidden instructions, API keys,
or implementation details to the candidate.

### V. Interview Flow

The interview MUST follow a controlled conversational flow.

A typical interview SHOULD follow:

Candidate information
→ Experience level selection
→ Dynamic instruction generation
→ AI interviewer
→ Question
→ Candidate answer
→ Evaluation/next question
→ Interview completion
→ Interview summary

The interviewer MUST remain consistent with the selected experience level
throughout the interview.

The system SHOULD avoid repeatedly asking the same question unless repetition
is intentionally required.

The interview SHOULD have a configurable maximum number of questions so that
the conversation does not continue indefinitely.

### VI. Separation of Responsibilities

The project MUST maintain clear separation between the UI, application
logic, agent logic, and data handling.

The UI MUST NOT contain core agent logic.

The agent MUST NOT directly depend on presentation-specific UI code.

Dynamic instruction construction SHOULD be isolated from UI components so that
interview behavior can be changed without rewriting the interface.

Data persistence SHOULD be isolated from the agent implementation.

### VII. Security and Privacy

Candidate information MUST be treated as sensitive application data.

The application MUST NOT expose API keys or credentials in frontend code.

Secrets MUST be stored using environment variables or an appropriate secret
management mechanism.

Candidate information MUST NOT be unnecessarily logged.

The application MUST avoid storing sensitive candidate information unless
required by the project requirements.

The UI MUST never display system instructions, internal prompts, or hidden
agent configuration.

### VIII. Simplicity and Educational Value

The project MUST remain small enough to understand and demonstrate clearly.

Every architectural component MUST have a clear purpose.

The project SHOULD prefer simple solutions over unnecessary abstractions,
microservices, databases, or additional agents.

Features MUST NOT be added merely to make the project appear more complex.

The primary goal is to demonstrate Agentic AI concepts correctly, especially
dynamic instructions, rather than building a production-scale HR platform.

### IX. Testability and Reliability

Core functionality MUST be testable independently from the UI.

At minimum, the project MUST test:
- Experience-level selection
- Dynamic instruction generation
- Interview initialization
- Question generation
- Interview progression
- Interview completion
- Invalid or missing input handling

The system MUST fail gracefully when an AI/API request fails.

The UI MUST provide a meaningful error state instead of exposing raw
exceptions or internal implementation details.

### X. Maintainability

Code MUST follow clear naming, modular structure, and reasonable documentation.

Configuration values MUST NOT be scattered throughout the codebase.

Prompts and dynamic instruction templates SHOULD be organized so they can be
modified without rewriting unrelated application logic.

Dependencies SHOULD be kept to the minimum necessary for the project.

## Governance

These principles are binding for the project.

If a proposed implementation conflicts with a principle, the specification,
plan, or implementation MUST be changed rather than silently ignoring the
principle.

The constitution MUST be reviewed whenever the project's fundamental
architecture or requirements change.

Technology-specific implementation decisions belong in the implementation
plan unless explicitly established by this constitution.

## Success Criteria

The project is considered successful when a user can:

1. Open the HR interview application.
2. Enter candidate information.
3. Select an experience level.
4. Start an interview.
5. Observe the AI interviewer adapt its behavior to the selected level.
6. Answer multiple interview questions through the UI.
7. Complete the interview.
8. Receive a useful interview summary or result.

The project MUST clearly demonstrate that the interviewer's instructions are
dynamically adapted according to the candidate's selected experience level.

## Development Principle

Build the smallest working version first.

The project should begin with one Google ADK structured interviewer agent and dynamic
instructions. Additional features should only be introduced when they are
supported by the specification and provide clear value.