import pandas as pd
import joblib
from pathlib import Path

from .feature_engineering import create_match_features
from .database import get_students, get_mentors


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# Load the trained ML model
# --------------------------------------------------

model = joblib.load(
    BASE_DIR / "models" / "mentor_model.pkl"
)


# --------------------------------------------------
# Recommendation function
# --------------------------------------------------
def recommend_mentors(student_id, top_n=5):

    # Get the latest data from PostgreSQL
    students = pd.DataFrame(
        get_students(),
        columns=[
            "student_id",
            "name",
            "career_goal",
            "skills",
            "interests",
            "experience_level",
            "preferred_industry",
            "availability"
        ]
    )

    mentors = pd.DataFrame(
        get_mentors(),
        columns=[
            "mentor_id",
            "name",
            "current_role",
            "experience_years",
            "skills",
            "interests",
            "industry",
            "availability"
        ]
    )

    # Find the requested student
    matching_students = students[
        students["student_id"] == student_id
    ]

    if matching_students.empty:
        return pd.DataFrame(
            columns=[
                "mentor_id",
                "mentor_name",
                "role",
                "match_probability",
                "reasons"
            ]
        )

    student = matching_students.iloc[0]

    recommendations = []

    # Compare the student with every mentor
    for _, mentor in mentors.iterrows():

        # Create matching features
        features = create_match_features(
            student,
            mentor
        )

        # Convert features into DataFrame
        feature_df = pd.DataFrame(
            [features]
        )

        # Predict probability of being a good match
        probability = model.predict_proba(
            feature_df
        )[0][1]

        # Generate explanations
        reasons = explain_match(
            student,
            mentor
        )

        recommendations.append({
            "mentor_id": mentor["mentor_id"],
            "mentor_name": mentor["name"],
            "role": mentor["current_role"],
            "match_probability": probability,
            "reasons": reasons
        })

    # Convert recommendations to DataFrame
    recommendations_df = pd.DataFrame(
        recommendations
    )

    # Sort highest match first
    recommendations_df = recommendations_df.sort_values(
        "match_probability",
        ascending=False
    )

    # Return top N mentors
    return recommendations_df.head(top_n)

# --------------------------------------------------
# Explain why a mentor was recommended
# --------------------------------------------------

def explain_match(student, mentor):

    features = create_match_features(
        student,
        mentor
    )

    reasons = []

    # Skill explanation
    if features["skill_overlap"] >= 0.7:
        reasons.append("Strong skill overlap")

    elif features["skill_overlap"] >= 0.4:
        reasons.append("Good skill overlap")

    else:
        reasons.append("Limited skill overlap")

    # Career goal explanation
    if features["career_goal_match"] == 1:
        reasons.append("Career goal is aligned")

    else:
        reasons.append(
            "Career goal is not directly aligned"
        )

    # Industry explanation
    if features["industry_match"] == 1:
        reasons.append("Same preferred industry")

    else:
        reasons.append("Different industry")

    # Interest explanation
    if features["interest_match"] >= 0.5:
        reasons.append("Shared interests")

    else:
        reasons.append("Limited shared interests")

    # Experience explanation
    if features["experience_fit"] >= 0.8:
        reasons.append("Strong experience fit")

    elif features["experience_fit"] >= 0.6:
        reasons.append("Good experience fit")

    else:
        reasons.append("Lower experience fit")

    # Availability explanation
    if features["availability_match"] == 1:
        reasons.append("Availability matches")

    else:
        reasons.append(
            "Availability does not match"
        )

    return reasons