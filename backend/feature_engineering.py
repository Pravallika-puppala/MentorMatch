import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# =========================================================
# 1. SKILL OVERLAP
# =========================================================

def calculate_skill_overlap(student_skills, mentor_skills):

    student_skills = set(
        skill.strip().lower()
        for skill in student_skills.split(",")
    )

    mentor_skills = set(
        skill.strip().lower()
        for skill in mentor_skills.split(",")
    )

    common_skills = student_skills.intersection(
        mentor_skills
    )

    if len(student_skills) == 0:
        return 0

    return len(common_skills) / len(student_skills)


# =========================================================
# 2. CAREER GOAL MATCH
# =========================================================

career_mapping = {

    "AI Engineer": [
        "AI Engineer",
        "ML Engineer",
        "AI Researcher"
    ],

    "ML Engineer": [
        "ML Engineer",
        "AI Engineer",
        "Data Scientist"
    ],

    "Data Scientist": [
        "Data Scientist",
        "ML Engineer",
        "AI Researcher"
    ],

    "Software Engineer": [
        "Software Engineer",
        "Backend Engineer",
        "Full Stack Engineer"
    ],

    "Backend Engineer": [
        "Backend Engineer",
        "Software Engineer"
    ],

    "Cloud Engineer": [
        "Cloud Engineer",
        "DevOps Engineer",
        "Cloud Architect"
    ],

    "DevOps Engineer": [
        "DevOps Engineer",
        "Cloud Engineer",
        "Cloud Architect"
    ],

    "Product Manager": [
        "Product Manager"
    ],

    "UX Designer": [
        "UX Designer",
        "UX Researcher",
        "Product Designer"
    ],

    "Product Designer": [
        "Product Designer",
        "UX Designer",
        "UX Researcher"
    ],

    "Data Analyst": [
        "Data Analyst",
        "Business Analyst",
        "Data Scientist"
    ],

    "Business Analyst": [
        "Business Analyst",
        "Data Analyst"
    ],

    "Cybersecurity Analyst": [
        "Cybersecurity Analyst",
        "Cybersecurity Engineer"
    ],

    "Cybersecurity Engineer": [
        "Cybersecurity Engineer",
        "Cybersecurity Analyst"
    ]
}


def calculate_career_goal_match(
    student_goal,
    mentor_role
):

    matching_roles = career_mapping.get(
        student_goal,
        []
    )

    if mentor_role in matching_roles:
        return 1

    return 0


# =========================================================
# 3. INDUSTRY MATCH
# =========================================================

def calculate_industry_match(
    student_industry,
    mentor_industry
):

    if student_industry.lower() == mentor_industry.lower():
        return 1

    return 0


# =========================================================
# 4. INTEREST MATCH
# =========================================================

def calculate_interest_match(
    student_interests,
    mentor_interests
):

    student_interests = set(
        interest.strip().lower()
        for interest in student_interests.split(",")
    )

    mentor_interests = set(
        interest.strip().lower()
        for interest in mentor_interests.split(",")
    )

    common_interests = student_interests.intersection(
        mentor_interests
    )

    if len(student_interests) == 0:
        return 0

    return len(common_interests) / len(student_interests)


# =========================================================
# 5. EXPERIENCE FIT
# =========================================================

def calculate_experience_fit(
    student_level,
    mentor_years
):

    if student_level == "Beginner":

        if mentor_years <= 3:
            return 1.0

        elif mentor_years <= 6:
            return 0.8

        else:
            return 0.6

    elif student_level == "Intermediate":

        if mentor_years <= 3:
            return 0.6

        elif mentor_years <= 6:
            return 1.0

        else:
            return 0.8

    elif student_level == "Advanced":

        if mentor_years <= 3:
            return 0.5

        elif mentor_years <= 6:
            return 0.8

        else:
            return 1.0

    return 0


# =========================================================
# 6. AVAILABILITY MATCH
# =========================================================

def calculate_availability_match(
    student_availability,
    mentor_availability
):

    if (
        student_availability.lower()
        == mentor_availability.lower()
    ):
        return 1

    return 0


# =========================================================
# 7. CREATE FEATURES FOR ONE PAIR
# =========================================================

def create_match_features(
    student,
    mentor
):

    skill_score = calculate_skill_overlap(
        student["skills"],
        mentor["skills"]
    )

    career_score = calculate_career_goal_match(
        student["career_goal"],
        mentor["current_role"]
    )

    industry_score = calculate_industry_match(
        student["preferred_industry"],
        mentor["industry"]
    )

    interest_score = calculate_interest_match(
        student["interests"],
        mentor["interests"]
    )

    experience_score = calculate_experience_fit(
        student["experience_level"],
        mentor["experience_years"]
    )

    availability_score = calculate_availability_match(
        student["availability"],
        mentor["availability"]
    )

    return {
        "skill_overlap": skill_score,
        "career_goal_match": career_score,
        "industry_match": industry_score,
        "interest_match": interest_score,
        "experience_fit": experience_score,
        "availability_match": availability_score
    }


# =========================================================
# 8. GENERATE TRAINING DATASET
# =========================================================

def generate_training_dataset():

    # Load CSV files only when we actually
    # want to generate training data
    students = pd.read_csv(
        DATA_DIR / "students.csv"
    )

    mentors = pd.read_csv(
        DATA_DIR / "mentor.csv"
    )

    all_matches = []

    # Generate every student-mentor combination
    for _, student in students.iterrows():

        for _, mentor in mentors.iterrows():

            features = create_match_features(
                student,
                mentor
            )

            match = {
                "student_id": student["student_id"],
                "mentor_id": mentor["mentor_id"],
                **features
            }

            all_matches.append(match)

    matches_df = pd.DataFrame(
        all_matches
    )

    print(
        "Total Matches:",
        len(matches_df)
    )


    # =====================================================
    # COMPATIBILITY SCORE
    # =====================================================

    matches_df["compatibility_score"] = (
        matches_df["skill_overlap"] * 0.30
        + matches_df["career_goal_match"] * 0.25
        + matches_df["industry_match"] * 0.15
        + matches_df["interest_match"] * 0.10
        + matches_df["experience_fit"] * 0.10
        + matches_df["availability_match"] * 0.10
    )


    # =====================================================
    # TARGET LABEL
    # =====================================================

    matches_df["good_match"] = (
        matches_df["compatibility_score"] >= 0.60
    ).astype(int)


    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    print("\nFirst 5 Matches:")
    print(matches_df.head())

    print("\nGood Match Distribution:")
    print(
        matches_df["good_match"].value_counts()
    )


    # =====================================================
    # SAVE DATASET
    # =====================================================

    output_path = (
        DATA_DIR / "match_training_data.csv"
    )

    matches_df.to_csv(
        output_path,
        index=False
    )

    print(
        "\nTraining dataset saved successfully!"
    )

    print(
        "Saved to:",
        output_path
    )

    return matches_df


# =========================================================
# RUN DATASET GENERATION ONLY WHEN THIS FILE
# IS EXECUTED DIRECTLY
# =========================================================

if __name__ == "__main__":

    generate_training_dataset()