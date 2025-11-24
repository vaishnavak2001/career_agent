"""Interview preparation endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.interview_prep import interview_service
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter()

class InterviewRequest(BaseModel):
    job_title: str
    company: str
    job_description: str

class FeedbackRequest(BaseModel):
    job_title: str
    question: str
    answer: str

@router.post("/questions")
async def generate_interview_questions(
    request: InterviewRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate interview questions for a specific job."""
    return await interview_service.generate_questions(
        request.job_title,
        request.company,
        request.job_description
    )

@router.post("/feedback")
async def get_answer_feedback(
    request: FeedbackRequest,
    current_user: User = Depends(get_current_user)
):
    """Get feedback on an interview answer."""
    return await interview_service.simulate_interview(
        request.job_title,
        request.answer,
        request.question
    )
