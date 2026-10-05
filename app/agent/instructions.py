from typing import Optional
from app.models.interview import ExperienceLevel

def build_interview_instructions(
    experience_level: ExperienceLevel,
    job_role: str,
    candidate_context: Optional[dict] = None
) -> str:
    """
    Dynamically build the system instructions for the Google ADK Interviewer Agent
    based on the candidate's chosen experience level and job role.
    """
    name = "the candidate"
    if candidate_context and "name" in candidate_context:
        name = candidate_context["name"]

    base_instructions = (
        f"You are an AI HR Interviewer conducting a screening interview for {name}, "
        f"who is applying for the role of {job_role}.\n"
        "Your goal is to evaluate the candidate across 5 questions total.\n"
        "Ask exactly ONE question at a time. Do not answer questions on behalf of the candidate.\n"
    )

    if experience_level == ExperienceLevel.ENTRY:
        level_instructions = (
            "Because this is an Entry Level interview, please adopt a friendly and encouraging tone. "
            "Focus on fundamental questions and their potential to learn. "
            "Avoid unnecessary difficulty or overly complex architectural questions. "
            "Help reduce the candidate's anxiety."
        )
    elif experience_level == ExperienceLevel.MID:
        level_instructions = (
            "Because this is a Mid Level interview, maintain a professional tone and present moderate difficulty. "
            "Include practical scenarios to test both their conceptual knowledge and practical experience."
        )
    elif experience_level == ExperienceLevel.SENIOR:
        level_instructions = (
            "Because this is a Senior Level interview, maintain a rigorous professional tone. "
            "Ask advanced questions and present complex scenarios. "
            "Test their technical depth, decision-making, and leadership capabilities where relevant."
        )
    else:
        # Fallback
        level_instructions = "Maintain a professional interviewing tone."

    return f"{base_instructions}\n{level_instructions}"
