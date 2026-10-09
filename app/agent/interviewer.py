import os
from typing import Optional, List
from app.models.interview import InterviewState
from app.agent.instructions import build_interview_instructions

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class InterviewerAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if HAS_GENAI and self.api_key and self.api_key != "your_gemini_api_key_here":
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def _get_system_instruction(self, interview_state: InterviewState) -> str:
        """Helper to build dynamic instructions on the fly."""
        context = {"name": interview_state.candidate.name}
        return build_interview_instructions(
            experience_level=interview_state.candidate.experience_level,
            job_role=interview_state.candidate.job_role,
            candidate_context=context
        )

    def _build_chat_history(self, interview_state: InterviewState) -> List["types.Content"]:
        """Reconstruct the Gemini conversation history from the state."""
        history = []
        if not HAS_GENAI:
            return history

        # The state arrays might not be the same length (questions leads answers).
        # We need to zip them carefully up to the answered point.
        for i, q in enumerate(interview_state.questions):
            history.append(
                types.Content(role="model", parts=[types.Part.from_text(text=q)])
            )
            if i < len(interview_state.answers):
                history.append(
                    types.Content(role="user", parts=[types.Part.from_text(text=interview_state.answers[i])])
                )
        return history

    def generate_first_question(self, interview_state: InterviewState) -> str:
        """Generates the initial interview greeting and first question."""
        if not self.client:
            # Fallback for testing/missing API environments
            return f"Welcome {interview_state.candidate.name}, to start, could you tell me about your experience as a {interview_state.candidate.job_role}?"

        instructions = self._get_system_instruction(interview_state)

        # We don't have history yet, simply send an initialization prompt
        config = types.GenerateContentConfig(
            system_instruction=instructions,
            temperature=0.7
        )

        prompt = "Hello, please introduce yourself briefly and ask the very first interview question."

        def _send():
            chat = self.client.chats.create(model="gemini-3.8-flash", config=config)
            return chat.send_message(prompt)

        import time
        response = None
        for attempt in range(3):
            try:
                response = _send()
                break
            except Exception as e:
                print(f"Failed to generate first question (attempt {attempt+1}): {e}")
                if attempt == 2:
                    return f"Welcome {interview_state.candidate.name}, to start, could you tell me about your experience as a {interview_state.candidate.job_role}?"
                time.sleep(1)

        if response and response.text:
            return response.text
        return "Can you tell me about yourself?"

    def generate_next_question(self, interview_state: InterviewState) -> str:
        """Generates the next question factoring in history."""
        if not self.client:
            # Fallback for testing/missing API environments
            return f"Thank you for that answer. Here is generic generated question {interview_state.current_question_number}."

        instructions = self._get_system_instruction(interview_state)
        history = self._build_chat_history(interview_state)

        # When sending the next turn via .chats.create(history=history), the last history turn should NOT
        # be the user's latest answer if we are about to trigger send_message with it.
        # However, it's easier to simply pass the whole history minus the very latest answer to the chat,
        # then send_message() with that latest answer.

        # Check if we have answers
        if not interview_state.answers:
            return self.generate_first_question(interview_state)

        latest_answer = interview_state.answers[-1]

        # Build history EXCLUDING the latest answer (and the last question if it pairs with it, wait...
        # history array already has model->q1, user->a1, model->q2, user->a2...
        # Let's rebuild history exactly up to the last question

        chat_history = []
        for i in range(len(interview_state.answers) - 1):
            chat_history.append(
                types.Content(role="model", parts=[types.Part.from_text(text=interview_state.questions[i])])
            )
            chat_history.append(
                types.Content(role="user", parts=[types.Part.from_text(text=interview_state.answers[i])])
            )

        # Add the latest question to history
        chat_history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=interview_state.questions[-1])])
        )

        config = types.GenerateContentConfig(
            system_instruction=instructions,
            temperature=0.7
        )

        chat = self.client.chats.create(
            model="gemini-3.8-flash",
            config=config,
            history=chat_history
        )

        # The prompt is the candidate's latest answer, plus a directive to ask the next question
        prompt = (
            f"Candidate Response: {latest_answer}\n\n"
            f"This is question {interview_state.current_question_number} of {interview_state.total_questions}. "
            "Please respond naturally to the candidate's answer above, then ask the next question. Do not repeat previous questions."
        )

        import time
        response = None
        for attempt in range(3):
            try:
                response = chat.send_message(prompt)
                break
            except Exception as e:
                print(f"Failed to generate next question (attempt {attempt+1}): {e}")
                if attempt == 2:
                    return f"Thank you for that answer. Here is generic generated question {interview_state.current_question_number}."
                time.sleep(1)

        if response and response.text:
            return response.text
        return "Thank you. Let's move to the next topic."
