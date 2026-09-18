import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .database import get_students
from .recommendation import recommend_mentors


# ==========================================================
# Gemini setup
# ==========================================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-3.6-flash"
# ==========================================================
# TOOL 1: Get student profile
# ==========================================================

def get_student_profile(student_id: str) -> dict:
    """
    Retrieves a student's profile from the MentorMatch database.

    Args:
        student_id: The unique ID of the student, for example S031.

    Returns:
        A dictionary containing the student's profile.
    """

    students = get_students()

    for student in students:

        if student[0] == student_id:

            return {
                "student_id": student[0],
                "name": student[1],
                "career_goal": student[2],
                "skills": student[3],
                "interests": student[4],
                "experience_level": student[5],
                "preferred_industry": student[6],
                "availability": student[7]
            }

    return {
        "error": "Student not found"
    }


# ==========================================================
# TOOL 2: Get mentor recommendations
# ==========================================================

def get_student_recommendations(student_id: str) -> list:
    """
    Retrieves the top mentor recommendations generated
    by the MentorMatch machine-learning model.

    Args:
        student_id: The unique ID of the student, for example S031.

    Returns:
        A list containing the recommended mentors.
    """

    recommendations = recommend_mentors(
        student_id,
        top_n=5
    )

    if recommendations.empty:
        return []

    return recommendations.to_dict(
        orient="records"
    )


# ==========================================================
# AI COMPANION
# ==========================================================

def ask_gemini(
    student_id: str,
    message: str
) -> str:

    # ------------------------------------------------------
    # System instructions
    # ------------------------------------------------------

    system_instruction = f"""
You are the AI Companion inside MentorMatch.

You are assisting student {student_id}.

Your job is to help the student with mentorship and career
guidance using the information available through your tools.

You can:

1. Retrieve the student's profile.
2. Retrieve the student's mentor recommendations.
3. Explain why recommended mentors may be suitable.
4. Help the student prepare questions for mentors.
5. Help the student think about their career goals.
6. Help the student understand their recommendations.

IMPORTANT RULES:

- Use tools whenever you need student-specific information.
- Never invent student information.
- Never invent mentor information.
- The machine-learning recommendation engine determines
  mentor compatibility.
- You explain and interpret the recommendation; you do not
  replace the recommendation engine.
- A match probability is not a guarantee of a successful
  mentorship.
- Keep answers practical and easy to understand.
- Do not expose unnecessary internal system details.
- The current student is {student_id}.
"""

    # ------------------------------------------------------
    # Gemini configuration
    # ------------------------------------------------------

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,

        tools=[
            get_student_profile,
            get_student_recommendations
        ]
    )

    # ------------------------------------------------------
    # Ask Gemini
    # ------------------------------------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=message,
        config=config
    )

    return response.text


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    student_id = "S031"

    message = (
        "Tell me about my profile and "
        "which mentors you recommend for me."
    )

    answer = ask_gemini(
        student_id,
        message
    )

    print("\n")
    print("=" * 60)
    print("MENTORMATCH AI COMPANION")
    print("=" * 60)

    print(answer)

    print("=" * 60)