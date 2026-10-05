from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, constr


class ExperienceLevel(str, Enum):
    ENTRY = "Entry Level"
    MID = "Mid Level"
    SENIOR = "Senior Level"


class VoiceState(str, Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    AI_SPEAKING = "AI_SPEAKING"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"


class CandidateInfo(BaseModel):
    name: str = Field(..., min_length=1, description="Candidate full name")
    job_role: str = Field(..., min_length=1, description="Title applied for")
    experience_level: ExperienceLevel


class InterviewState(BaseModel):
    interview_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate: CandidateInfo
    current_question_number: int = Field(default=1, ge=1, le=5)
    total_questions: int = 5
    questions: List[str] = Field(default_factory=list)
    answers: List[str] = Field(default_factory=list)
    status: VoiceState = Field(default=VoiceState.IDLE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_question(self, question: str):
        if self.status == VoiceState.COMPLETED:
            raise ValueError("Interview is already completed.")
        self.questions.append(question)
        if len(self.questions) == 1:
            self.status = VoiceState.AI_SPEAKING

    def add_answer(self, answer: str):
        if self.status == VoiceState.COMPLETED:
            raise ValueError("Interview is already completed.")

        self.answers.append(answer)

        if self.current_question_number < self.total_questions:
            self.current_question_number += 1
            self.status = VoiceState.PROCESSING
        else:
            self.status = VoiceState.COMPLETED


class InterviewAssessment(BaseModel):
    candidate_name: str
    applied_role: str
    experience_level: str
    overall_summary: str
    key_strengths: List[str]
    areas_for_improvement: List[str]
    overall_assessment: str
    disclaimer: str = "This is a screening aid, not a definitive hiring decision."
