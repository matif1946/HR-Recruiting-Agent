from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict

from app.models.interview import CandidateInfo, InterviewState, VoiceState, InterviewAssessment
from app.services.interview_service import InterviewService
from app.agent.interviewer import InterviewerAgent
try:
    from app.agent.assessment import AssessmentAgent
except ImportError:
    AssessmentAgent = None

router = APIRouter(prefix="/api/interviews", tags=["interviews"])

# Schemas for requests/responses
class AnswerSubmission(BaseModel):
    answer: str

class InterviewResponse(BaseModel):
    interview_id: str
    status: VoiceState
    current_question_number: int
    latest_question: Optional[str] = None
    is_completed: bool = False
    error: Optional[str] = None

class SetupInterviewRequest(CandidateInfo):
    pass

@router.post("", response_model=InterviewResponse)
def initialize_interview(candidate: SetupInterviewRequest):
    """Start a new interview session."""
    interview = InterviewService.create_interview(candidate)

    agent = InterviewerAgent()
    try:
        first_question = agent.generate_first_question(interview)
        interview.add_question(first_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "interview_id": interview.interview_id,
        "status": interview.status,
        "current_question_number": interview.current_question_number,
        "latest_question": first_question,
        "is_completed": False
    }

@router.get("/{interview_id}")
def get_interview_state(interview_id: str):
    """Get the current state of an interview."""
    interview = InterviewService.get_interview(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    latest_question = interview.questions[-1] if interview.questions else None

    response = {
        "interview_id": interview.interview_id,
        "status": interview.status,
        "current_question_number": interview.current_question_number,
        "latest_question": latest_question,
        "is_completed": interview.status == VoiceState.COMPLETED,
        "candidate": interview.candidate
    }

    if interview.status == VoiceState.COMPLETED and AssessmentAgent:
        # Check if assessment is already generated
        # We'll just generate on the fly or wait for a specific endpoint if needed.
        pass

    return response

@router.post("/{interview_id}/response", response_model=InterviewResponse)
def submit_answer(interview_id: str, submission: AnswerSubmission):
    """Submit an answer and get the next question or complete the interview."""
    interview = InterviewService.get_interview(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.status == VoiceState.COMPLETED:
        raise HTTPException(status_code=400, detail="Interview is already completed")

    # Process the answer
    try:
        InterviewService.process_answer(interview_id, submission.answer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # If completed, we don't generate a next question
    if interview.status == VoiceState.COMPLETED:
        return {
            "interview_id": interview.interview_id,
            "status": interview.status,
            "current_question_number": interview.current_question_number,
            "latest_question": None,
            "is_completed": True
        }

    # Generate next question
    agent = InterviewerAgent()
    try:
        next_question = agent.generate_next_question(interview)
        interview.add_question(next_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate next question: {str(e)}")

    return {
        "interview_id": interview.interview_id,
        "status": interview.status,
        "current_question_number": interview.current_question_number,
        "latest_question": next_question,
        "is_completed": False
    }

@router.post("/{interview_id}/end")
def end_interview(interview_id: str):
    """Early termination of an interview."""
    interview = InterviewService.end_interview(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    return {"status": "success", "interview_id": interview_id}

@router.get("/{interview_id}/assessment")
def get_assessment(interview_id: str):
    """Generate and retrieve the assessment for a completed interview."""
    interview = InterviewService.get_interview(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.status != VoiceState.COMPLETED:
        raise HTTPException(status_code=400, detail="Interview must be completed to generate an assessment")

    if not AssessmentAgent:
        raise HTTPException(status_code=500, detail="Assessment component not available")

    agent = AssessmentAgent()
    try:
        assessment = agent.generate_assessment(interview)
        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate assessment: {str(e)}")
