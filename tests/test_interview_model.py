import pytest
from app.models.interview import CandidateInfo, ExperienceLevel, VoiceState
from app.services.interview_service import InterviewService

def setup_function():
    # Clear in-memory storage before each test
    InterviewService.reset_storage()

def test_data_model_and_service():
    # 1. Create candidate info
    candidate = CandidateInfo(
        name="Atif",
        job_role="Python Developer",
        experience_level=ExperienceLevel.SENIOR
    )

    # 2. Create an interview
    interview = InterviewService.create_interview(candidate)

    assert interview.interview_id is not None
    assert interview.current_question_number == 1
    assert interview.total_questions == 5
    assert interview.status == VoiceState.IDLE

    # Verify we can retrieve it
    retrieved = InterviewService.get_interview(interview.interview_id)
    assert retrieved is not None
    assert retrieved.candidate.name == "Atif"
    assert retrieved.candidate.job_role == "Python Developer"
    assert retrieved.candidate.experience_level == ExperienceLevel.SENIOR

    # 3. Store questions
    interview.add_question("Could you describe your strategy for designing resilient multi-region cloud architectures?")
    assert len(interview.questions) == 1
    assert interview.status == VoiceState.AI_SPEAKING

    # 4. Store answers and move from Question 1 -> 2
    InterviewService.process_answer(interview.interview_id, "I typically use an active-active pattern with DynamoDB replication.")
    assert len(interview.answers) == 1
    assert interview.current_question_number == 2
    assert interview.status == VoiceState.PROCESSING

    # Simulate asking 2nd question
    interview.add_question("How do you handle conflict resolution during partitions?")

    # Process answers up to question 5
    InterviewService.process_answer(interview.interview_id, "Answer 2") # progress to Q3
    assert interview.current_question_number == 3

    interview.add_question("Question 3")
    InterviewService.process_answer(interview.interview_id, "Answer 3") # progress to Q4
    assert interview.current_question_number == 4

    interview.add_question("Question 4")
    InterviewService.process_answer(interview.interview_id, "Answer 4") # progress to Q5

    # 5. Detect question 5 and Mark interview completed
    assert interview.current_question_number == 5
    interview.add_question("Final Question")

    # Final answer
    InterviewService.process_answer(interview.interview_id, "Final Answer")
    assert interview.current_question_number == 5
    assert interview.status == VoiceState.COMPLETED

    # 6. Cannot add more answers/questions if completed
    with pytest.raises(ValueError, match="Interview is already completed"):
        interview.add_answer("Extra Answer")

    with pytest.raises(ValueError, match="Interview is already completed"):
        interview.add_question("Extra Question")

def test_input_validation():
    # Attempt to create candidate with incomplete data
    with pytest.raises(ValueError):
        CandidateInfo(name="", job_role="Python Developer", experience_level=ExperienceLevel.SENIOR)

    with pytest.raises(ValueError):
        CandidateInfo(name="Atif", job_role="", experience_level=ExperienceLevel.SENIOR)

