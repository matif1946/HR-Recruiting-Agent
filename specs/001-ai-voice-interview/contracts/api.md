# API Contracts

All endpoints return standard JSON responses and omit internal prompts or sensitive system configuration.

## 1. Create Interview
**Endpoint**: `POST /api/interviews`
**Purpose**: Starts a new interview session and generates the first AI question dynamically.

### Request Body
```json
{
  "name": "Sarah Connor",
  "job_role": "Cloud Architect",
  "experience_level": "Senior Level"
}
```

### Response Body (`201 Created`)
```json
{
  "interview_id": "8f3b219e-99e2-411a-8c88-e9f3bfa8bc19",
  "candidate": {
    "name": "Sarah Connor",
    "job_role": "Cloud Architect",
    "experience_level": "Senior Level"
  },
  "current_question_number": 1,
  "total_questions": 5,
  "current_question": "Welcome, Sarah. To start our conversation, could you describe your strategy for designing resilient multi-region cloud architectures for high-availability systems?",
  "status": "AI_SPEAKING"
}
```

---

## 2. Submit Response / Progress Interview
**Endpoint**: `POST /api/interviews/{interview_id}/response`
**Purpose**: Receives the candidate's answer (via speech-to-text string or fallback manual text input) and generates the next dynamic question or triggers assessment.

### Request Body
```json
{
  "answer": "I typically use an active-active pattern with Global Server Load Balancing and distributed DynamoDB replication across regions."
}
```

### Response Body (`200 OK`)
```json
{
  "interview_id": "8f3b219e-99e2-411a-8c88-e9f3bfa8bc19",
  "current_question_number": 2,
  "total_questions": 5,
  "next_question": "That makes sense. When using active-active patterns with distributed data, how do you approach consistency and conflict resolution during network partitions?",
  "is_completed": false,
  "status": "AI_SPEAKING"
}
```

*When the 5th question has been answered:*
```json
{
  "interview_id": "8f3b219e-99e2-411a-8c88-e9f3bfa8bc19",
  "current_question_number": 5,
  "total_questions": 5,
  "next_question": null,
  "is_completed": true,
  "assessment": {
    "candidate_name": "Sarah Connor",
    "applied_role": "Cloud Architect",
    "experience_level": "Senior Level",
    "overall_summary": "Demonstrated strong knowledge of high-availability cloud designs and modern distributed patterns.",
    "key_strengths": [
      "Deep understanding of multi-region redundancy",
      "Nuanced trade-off evaluation for distributed state"
    ],
    "areas_for_improvement": [
      "Could elaborate more on cost optimization considerations"
    ],
    "overall_assessment": "Strong candidate with comprehensive senior-level technical depth."
  },
  "status": "COMPLETED"
}
```

---

## 3. Retrieve Interview State
**Endpoint**: `GET /api/interviews/{interview_id}`
**Purpose**: Fetches the current session state.

### Response Body (`200 OK`)
```json
{
  "interview_id": "8f3b219e-99e2-411a-8c88-e9f3bfa8bc19",
  "candidate": {
    "name": "Sarah Connor",
    "job_role": "Cloud Architect",
    "experience_level": "Senior Level"
  },
  "current_question_number": 2,
  "total_questions": 5,
  "status": "IDLE"
}
```

---

## 4. End Interview Early
**Endpoint**: `POST /api/interviews/{interview_id}/end`
**Purpose**: Safely cancels or truncates an active interview session.

### Response Body (`200 OK`)
```json
{
  "interview_id": "8f3b219e-99e2-411a-8c88-e9f3bfa8bc19",
  "status": "COMPLETED",
  "message": "Interview terminated safely."
}
```
