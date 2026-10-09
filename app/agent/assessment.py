import os
import json
from typing import List, Dict, Any, Optional

from app.models.interview import InterviewState, InterviewAssessment

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AssessmentAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key and self.api_key != "your_gemini_api_key_here":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_assessment(self, interview_state: InterviewState) -> InterviewAssessment:
        if not self.client:
            return InterviewAssessment(
                candidate_name=interview_state.candidate.name,
                applied_role=interview_state.candidate.job_role,
                experience_level=interview_state.candidate.experience_level.value,
                overall_summary="The candidate completed the interview.",
                key_strengths=["Problem solving"],
                areas_for_improvement=["System design"],
                overall_assessment="Acceptable screening results."
            )

        instructions = (
            "You are an expert strict Technical Recruiter and HR Evaluator AI. "
            "You have just completed a screening interview with a candidate for the role of '{job_role}' at the '{experience_level}' level. "
            "Your job is to provide a ruthless, accurate, and objective assessment based ONLY on the transcript provided.\n\n"
            "Rules for evaluation:\n"
            "1. If the candidate gives generic, short, or technically shallow answers, call this out in areas for improvement.\n"
            "2. If the candidate answers fewer than {total_qs} questions (e.g. they ended the interview early), explicitly state that the interview was incomplete and they aborted early.\n"
            "3. DO NOT hallucinate strengths that are not explicitly proven in the transcript.\n"
            "4. In the 'overall_assessment' field, you MUST start with either 'RECOMMENDED TO PROCEED' or 'NOT RECOMMENDED'. Be highly critical. Only recommend if they gave comprehensive, high-quality answers. If the interview was aborted early or answers were poor, output 'NOT RECOMMENDED'.\n"
            "5. The output must perfectly match the requested JSON schema."
        ).format(
            job_role=interview_state.candidate.job_role,
            experience_level=interview_state.candidate.experience_level.value,
            total_qs=interview_state.total_questions
        )

        transcript = ""
        questions_answered = len(interview_state.answers)
        if questions_answered == 0:
            transcript = "Candidate provided no answers and left the interview."
        else:
            for index in range(questions_answered):
                transcript += f"Q: {interview_state.questions[index]}\n"
                transcript += f"A: {interview_state.answers[index]}\n\n"

        prompt = (
            f"Candidate Name: {interview_state.candidate.name}\n"
            f"Questions Answered: {questions_answered} out of {interview_state.total_questions}\n"
            f"Transcript:\n{transcript}\n\n"
            "Based on the transcript above, please generate the assessment in JSON format with exactly these keys: "
            "'overall_summary' (string), 'key_strengths' (list of strings), "
            "'areas_for_improvement' (list of strings), 'overall_assessment' (string)."
        )

        config = types.GenerateContentConfig(
            system_instruction=instructions,
            temperature=0.1,
            response_mime_type="application/json"
        )

        chat = self.client.chats.create(model="gemini-1.5-flash", config=config)

        import time
        response = None
        last_err = None
        for attempt in range(3):
            try:
                response = chat.send_message(prompt)
                break
            except Exception as e:
                last_err = e
                time.sleep(1)

        try:
            if not response:
                raise last_err
            data = json.loads(response.text)
            return InterviewAssessment(
                candidate_name=interview_state.candidate.name,
                applied_role=interview_state.candidate.job_role,
                experience_level=interview_state.candidate.experience_level.value,
                overall_summary=data.get("overall_summary", "Summary unavailable."),
                key_strengths=data.get("key_strengths", []),
                areas_for_improvement=data.get("areas_for_improvement", []),
                overall_assessment=data.get("overall_assessment", "Assessment unavailable.")
            )
        except Exception as e:
            print(f"Error generating assessment: {e}")
            return InterviewAssessment(
                candidate_name=interview_state.candidate.name,
                applied_role=interview_state.candidate.job_role,
                experience_level=interview_state.candidate.experience_level.value,
                overall_summary="Error generating assessment.",
                key_strengths=[],
                areas_for_improvement=[],
                overall_assessment="Error processing results."
            )
