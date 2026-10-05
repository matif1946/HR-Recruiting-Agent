from app.models.interview import ExperienceLevel
from app.agent.instructions import build_interview_instructions

def test_dynamic_instructions():
    role = "Python Developer"
    context = {"name": "Test Candidate"}

    entry_instructions = build_interview_instructions(ExperienceLevel.ENTRY, role, context)
    mid_instructions = build_interview_instructions(ExperienceLevel.MID, role, context)
    senior_instructions = build_interview_instructions(ExperienceLevel.SENIOR, role, context)

    # Verify they are all different
    assert entry_instructions != mid_instructions
    assert mid_instructions != senior_instructions
    assert entry_instructions != senior_instructions

    # Verify presence of level-specific directives
    assert "friendly and encouraging" in entry_instructions
    assert "fundamental questions" in entry_instructions

    assert "moderate difficulty" in mid_instructions
    assert "practical scenarios" in mid_instructions

    assert "rigorous" in senior_instructions
    assert "advanced questions" in senior_instructions
    assert "decision-making" in senior_instructions

    # Verify common role integration
    assert "Python Developer" in entry_instructions
    assert "Python Developer" in mid_instructions
    assert "Python Developer" in senior_instructions
    assert "Test Candidate" in entry_instructions
