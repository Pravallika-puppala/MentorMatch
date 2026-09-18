from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .ai_companion import ask_gemini
from .recommendation import recommend_mentors
from .database import create_student


# ==========================================================
# FastAPI application
# ==========================================================

app = FastAPI(
    title="MentorMatch API",
    description="AI-powered student mentor recommendation platform",
    version="1.0.0"
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Request models
# ==========================================================

class CompanionRequest(BaseModel):
    message: str


class StudentCreate(BaseModel):
    student_id: str
    name: str
    career_goal: str
    skills: str
    interests: str
    experience_level: str
    preferred_industry: str
    availability: str


# ==========================================================
# Home endpoint
# ==========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to MentorMatch API"
    }


# ==========================================================
# Create a new student
# ==========================================================

@app.post("/students")
def create_new_student(student: StudentCreate):

    create_student(
        student.student_id,
        student.name,
        student.career_goal,
        student.skills,
        student.interests,
        student.experience_level,
        student.preferred_industry,
        student.availability
    )

    return {
        "message": "Student created successfully",
        "student_id": student.student_id
    }


# ==========================================================
# Get mentor recommendations
# ==========================================================

@app.get("/students/{student_id}/recommendations")
def get_recommendations(student_id: str):

    recommendations = recommend_mentors(
        student_id,
        top_n=5
    )

    if recommendations.empty:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return recommendations.to_dict(
        orient="records"
    )


# ==========================================================
# AI Companion
# ==========================================================

@app.post("/students/{student_id}/companion")
def companion(
    student_id: str,
    request: CompanionRequest
):

    answer = ask_gemini(
        student_id,
        request.message
    )

    return {
        "student_id": student_id,
        "response": answer
    }