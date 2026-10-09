import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_error_handling():
    # T050: Test API error handling on bad data
    response = client.post("/api/interviews", json={
        "name": "",
        "job_role": "Dev",
        "experience_level": "Entry Level"
    })
    assert response.status_code == 422 # FastAPI built-in handler

    response = client.post("/api/interviews", json={
        "name": "Jane",
        "job_role": "",
        "experience_level": "Entry Level"
    })
    assert response.status_code == 422

    response = client.post("/api/interviews/invalid-uuid-123/response", json={"answer": "hello"})
    assert response.status_code == 404

def test_voice_failure_scenarios_and_text_fallback():
    # T051 & T052: Voice failure uses text exact same backend pipeline
    # Setup interview
    response = client.post("/api/interviews", json={
        "name": "Fallback User",
        "job_role": "Backend",
        "experience_level": "Senior Level"
    })
    assert response.status_code == 200
    interview_id = response.json()["interview_id"]

    # Submit via text fallback (same endpoint as voice processing result)
    resp2 = client.post(f"/api/interviews/{interview_id}/response", json={
        "answer": "This is a text fallback answer because voice failed."
    })
    assert resp2.status_code == 200
    assert resp2.json()["current_question_number"] == 2

def test_complete_end_to_end_interview():
    # T047, T048, T049, T053: Complete E2E progression
    # 1. Setup
    res = client.post("/api/interviews", json={
        "name": "E2E Tester",
        "job_role": "Fullstack",
        "experience_level": "Mid Level"
    })
    assert res.status_code == 200
    interview_id = res.json()["interview_id"]
    
    # Check GET state
    state_res = client.get(f"/api/interviews/{interview_id}")
    assert state_res.status_code == 200
    assert state_res.json()["candidate"]["name"] == "E2E Tester"

    # 2. Answer 4 questions to reach limit 
    for i in range(4):
        ans = client.post(f"/api/interviews/{interview_id}/response", json={
            "answer": f"E2E answer {i}"
        })
        assert ans.status_code == 200
        
        if i < 3:
            assert ans.json()["is_completed"] is False
            assert ans.json()["current_question_number"] == i + 2
        else:
            # 5th question answered (i=3 was the 4th, wait:
            # Q1 created at setup.
            # Ans1 -> creates Q2
            # Ans2 -> creates Q3
            # Ans3 -> creates Q4
            # Ans4 -> creates Q5
            assert ans.json()["current_question_number"] == 5
            
    # Submit 5th answer
    final_ans = client.post(f"/api/interviews/{interview_id}/response", json={
            "answer": "Final answer 5"
    })
    
    assert final_ans.status_code == 200
    assert final_ans.json()["is_completed"] is True
    
    # 3. Assessment
    assessment = client.get(f"/api/interviews/{interview_id}/assessment")
    assert assessment.status_code == 200
    data = assessment.json()
    assert "overall_summary" in data
    assert "key_strengths" in data
    assert "areas_for_improvement" in data
