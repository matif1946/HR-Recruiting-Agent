import pytest
from app.models.interview import CandidateInfo, ExperienceLevel, InterviewState
from app.agent.interviewer import InterviewerAgent

def test_interviewer_agent_fallback_mode():
    agent = InterviewerAgent()
    # Force client to None to test the deterministic fallback path
    agent.client = None

    candidate = CandidateInfo(
        name="Atif",
        job_role="Python Developer",
        experience_level=ExperienceLevel.MID
    )
    state = InterviewState(candidate=candidate)

    # 1. Generate first question
    first_q = agent.generate_first_question(state)
    assert "Atif" in first_q
    assert "Python Developer" in first_q
    state.add_question(first_q)

    # 2. Answer first question
    state.add_answer("I have 4 years of experience.")

    # 3. Generate next question
    next_q = agent.generate_next_question(state)
    assert "generic generated question 2" in next_q
    state.add_question(next_q)

    # 4. Progress and state tracking handled properly by the interviewer agent calls
    assert len(state.questions) == 2
    assert state.questions[0] == first_q
    assert state.questions[1] == next_q

