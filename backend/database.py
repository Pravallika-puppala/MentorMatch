import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


# Connect to PostgreSQL
def get_connection():
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )

    return connection

# Get all students
def get_students():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            student_id,
            name,
            career_goal,
            skills,
            interests,
            experience_level,
            preferred_industry,
            availability
        FROM students;
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students


# Get all mentors
def get_mentors():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            mentor_id,
            name,
            "current_role",
            experience_years,
            skills,
            interests,
            industry,
            availability
        FROM mentors;
    """)

    mentors = cursor.fetchall()

    cursor.close()
    connection.close()

    return mentors


# Test the database functions
if __name__ == "__main__":

    students = get_students()
    mentors = get_mentors()

    print("Students:", len(students))
    print("Mentors:", len(mentors))

    print("\nFirst student:")
    print(students[0])

    print("\nFirst mentor:")
    print(mentors[0])

    # Create a new student
def create_student(
    student_id,
    name,
    career_goal,
    skills,
    interests,
    experience_level,
    preferred_industry,
    availability
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students (
            student_id,
            name,
            career_goal,
            skills,
            interests,
            experience_level,
            preferred_industry,
            availability
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            student_id,
            name,
            career_goal,
            skills,
            interests,
            experience_level,
            preferred_industry,
            availability
        )
    )

    connection.commit()

    cursor.close()
    connection.close()