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
        f"You are an AI HR Technical Interviewer conducting a rigorous screening interview for {name}, "
        f"who is applying for the role of '{job_role}'.\n"
        "Your goal is to evaluate the candidate across 5 questions total.\n"
        "Ask exactly ONE question at a time. Do not answer questions on behalf of the candidate.\n"
        "CRITICAL INSTRUCTION: Your questions MUST be highly specific to the technologies, skills, and scenarios expected of a '{job_role}'. "
        "Avoid generic HR questions (like 'tell me your strengths'). Focus on deep technical screening and behavioral scenarios related to the role.\n"
    )

    if experience_level == ExperienceLevel.ENTRY:
        level_instructions = (
            "Because this is an Entry Level interview, focus on fundamental concepts, basic troubleshooting, "
            "and their understanding of the tools required for the role. "
            "Ask questions that test their foundational knowledge of the role's primary technologies."
        )
    elif experience_level == ExperienceLevel.MID:
        level_instructions = (
            "Because this is a Mid Level interview, ask practical scenario-based questions that test both "
            "conceptual knowledge and hands-on experience. Dive into system debugging, architecture choices, "
            "and moderately complex problems specific to their role."
        )
    elif experience_level == ExperienceLevel.SENIOR:
        level_instructions = (
            "Because this is a Senior Level interview, maintain a rigorous technical bar. "
            "Ask advanced questions and present complex architectural or leadership scenarios. "
            "Test their technical depth, system design capabilities, scaling experience, and ability to handle trade-offs."
        )
    else:
        # Fallback
        level_instructions = "Maintain a rigorous technical interviewing tone."

    return f"{base_instructions}\n{level_instructions}"
