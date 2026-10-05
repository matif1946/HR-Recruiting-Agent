from typing import Dict, Optional
from app.models.interview import InterviewState, CandidateInfo

# In-memory data store for the MVP
_interviews: Dict[str, InterviewState] = {}

class InterviewService:
    @classmethod
    def create_interview(cls, candidate: CandidateInfo) -> InterviewState:
        """Create a new interview session and store it in-memory."""
        interview = InterviewState(candidate=candidate)
        _interviews[interview.interview_id] = interview
        return interview

    @classmethod
    def get_interview(cls, interview_id: str) -> Optional[InterviewState]:
        """Lookup an interview session by ID."""
        return _interviews.get(interview_id)

    @classmethod
    def get_all_interviews(cls) -> Dict[str, InterviewState]:
        """Get all interviews (for testing/debug)."""
        return _interviews

    @classmethod
    def process_answer(cls, interview_id: str, answer: str) -> Optional[InterviewState]:
        """Record a candidate's answer and progress the interview."""
        interview = cls.get_interview(interview_id)
        if not interview:
            return None

        interview.add_answer(answer)
        return interview

    @classmethod
    def end_interview(cls, interview_id: str) -> Optional[InterviewState]:
        """Safely end or truncate an interview early."""
        interview = cls.get_interview(interview_id)
        if not interview:
            return None

        from app.models.interview import VoiceState
        interview.status = VoiceState.COMPLETED
        return interview

    @classmethod
    def reset_storage(cls) -> None:
        """Clear all interviews (useful for testing)."""
        _interviews.clear()
