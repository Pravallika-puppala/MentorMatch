
MentorMatch
 Intelligent Mentorship & Career Recommendation Platform

MentorMatch is an AI-powered mentorship recommendation platform that uses **Machine Learning, FastAPI, PostgreSQL, and Gemini AI** to connect students with relevant mentors based on their skills, career goals, interests, industry preferences, experience level, and availability.

The platform combines a **machine-learning recommendation engine** with an **AI Companion** that helps students understand their recommendations and prepare for mentorship conversations.

 Features

Intelligent Mentor Recommendation

Students create a profile containing:

- Career goal
- Skills
- Interests
- Experience level
- Preferred industry
- Availability

MentorMatch compares the student profile against available mentors and generates a compatibility score for each mentor.

The system returns the **Top 5 recommended mentors**.

 Machine Learning Recommendation Engine

The recommendation engine uses a **Random Forest Classifier** to predict mentor compatibility.

The matching system generates six features:

| Feature | Description |
|---|---|
| Skill Overlap | Measures how many of the student's skills overlap with the mentor's skills |
| Career Goal Match | Checks whether the mentor's role aligns with the student's career goal |
| Industry Match | Checks whether the student's preferred industry matches the mentor's industry |
| Interest Match | Measures shared interests |
| Experience Fit | Evaluates whether the mentor's experience level fits the student's experience |
| Availability Match | Checks whether student and mentor availability align |

The compatibility features are weighted as:

```text
Skill Overlap       → 30%
Career Goal Match   → 25%
Industry Match      → 15%
Interest Match      → 10%
Experience Fit      → 10%
Availability Match  → 10%
````

---
 Explainable Recommendations

MentorMatch does not only return a score.

For every recommended mentor, the platform explains **why the mentor was recommended**.

Example:

```text
✓ Good skill overlap
✓ Career goal is aligned
✓ Same preferred industry
✓ Shared interests
✓ Strong experience fit
✓ Availability matches
```

This makes the recommendation easier for students to understand instead of presenting a black-box score.

---

AI Companion

MentorMatch includes an AI Companion powered by **Google Gemini**.

The AI Companion is designed specifically around the mentorship workflow rather than functioning as a generic chatbot.

It can:

* Retrieve the student's profile
* Retrieve mentor recommendations
* Explain mentor recommendations
* Help students understand their matches
* Help prepare questions for mentors
* Help students think through career goals

The AI Companion uses controlled tools to retrieve student-specific information.

Important Architecture Decision

The ML recommendation engine determines **mentor compatibility**.

The AI Companion does **not** replace the recommendation engine.

Instead:

```text
ML Model
    ↓
Determines suitable mentors

AI Companion
    ↓
Explains and helps the student act on those recommendations
```

---

System Architecture

```text
                         ┌──────────────────────┐
                         │      Frontend        │
                         │     HTML/CSS/JS      │
                         └──────────┬───────────┘
                                    │
                                  REST API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
      ┌────────────────┐   ┌─────────────────┐   ┌────────────────┐
      │   PostgreSQL   │   │ Recommendation  │   │  Gemini API    │
      │                │   │     Engine      │   │                │
      │ Students       │   │                 │   │ AI Companion   │
      │ Mentors        │   │ Random Forest   │   │                │
      └────────────────┘   └─────────────────┘   └────────────────┘
 Recommendation Workflow

```text
Student creates profile
        ↓
FastAPI receives profile
        ↓
Profile stored in PostgreSQL
        ↓
Retrieve student + mentor profiles
        ↓
Generate matching features
        ↓
Random Forest model
        ↓
Predict mentor compatibility
        ↓
Rank mentors
        ↓
Return Top 5 mentors
        ↓
Generate "Why this mentor?" explanations
` AI Companion Workflow

```text
Student asks a question
        ↓
FastAPI
        ↓
Gemini AI Companion
        ↓
Determine whether student-specific information is needed
        ↓
Use controlled tools
        ↓
Retrieve profile / recommendations
        ↓
Generate practical response
`
  Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### Machine Learning

* Scikit-learn
* Pandas
* Joblib

### Database

* PostgreSQL
* Psycopg2

### Generative AI

* Google Gemini
* Google GenAI Python SDK

### Frontend

* HTML
* CSS
* JavaScript

### DevOps

* Docker
* Docker Compose
* Git
* GitHub

---

# 📁 Project Structure

```text
MentorMatch/
│
├── backend/
│   ├── ai_companion.py
│   ├── database.py
│   ├── feature_engineering.py
│   ├── main.py
│   ├── recommendation.py
│   └── train_model.py
│
├── data/
│   ├── students.csv
│   ├── mentor.csv
│   └── match_training_data.csv
│
├── models/
│   └── mentor_model.pkl
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

Database

MentorMatch uses PostgreSQL to store application data.

Students

The `students` table stores:

```text
student_id
name
career_goal
skills
interests
experience_level
preferred_industry
availability
```

 Mentors

The `mentors` table stores:

```text
mentor_id
name
current_role
experience_years
skills
interests
industry
availability
```

---

 API Endpoints

## Home

```http
GET /
```

Returns a basic API status message.

---

## Create Student

```http
POST /students
```

Creates a new student profile.

Example request:

```json
{
  "student_id": "S031",
  "name": "Test Student",
  "career_goal": "AI Engineer",
  "skills": "Python,ML,SQL",
  "interests": "AI,Startups",
  "experience_level": "Beginner",
  "preferred_industry": "Technology",
  "availability": "Weekends"
}
```

---
 Get Recommendations

```http
GET /students/{student_id}/recommendations
```

Returns the student's top mentor recommendations.

Example:

```text
GET /students/S031/recommendations
```

Response contains:

```json
[
  {
    "mentor_id": "M001",
    "mentor_name": "Rahul",
    "role": "ML Engineer",
    "match_probability": 0.99,
    "reasons": [
      "Good skill overlap",
      "Career goal is aligned",
      "Same preferred industry"
    ]
  }
]
```

---
 AI Companion

```http
POST /students/{student_id}/companion
```

Example request:

```json
{
  "message": "Which mentor would be relevant to my career goal?"
}
```

The AI Companion uses the student's available profile and recommendation information to generate a personalized response.

---

 Machine Learning Model

The project uses a Random Forest classifier as the initial recommendation model.

### Model configuration

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
```

The training dataset contains:

```text
30 Students
×
30 Mentors
=
900 Match Combinations
```

The current training dataset contains:

```text
799 Negative Matches
101 Positive Matches
```

The model is trained offline and saved as:

```text
models/mentor_model.pkl
```

The API loads the trained model during startup instead of retraining it for every request.

---

Recommendation Approach

The system currently uses synthetic training labels generated from a weighted compatibility rule.

This is an important limitation.

The current model demonstrates the **engineering pipeline for an ML-powered recommendation system**, but the resulting model performance should not be interpreted as proof of real-world mentorship success.

A future production version could replace the synthetic labels with real interaction data such as:

* Mentor acceptance
* Student feedback
* Completed mentorship sessions
* Student satisfaction
* Successful mentor-student interactions
* Long-term mentorship outcomes

This would allow the recommendation model to learn from actual user behavior.

---

 Security

Sensitive credentials are stored in environment variables rather than source code.

Example:

```env
GEMINI_API_KEY=your_api_key
POSTGRES_HOST=your_database_host
POSTGRES_DB=mentormatch
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
```

The `.env` file is excluded from Git using `.gitignore`.

```text
.env
venv/
__pycache__/
*.pyc
```

**Never commit API keys, database passwords, or other secrets to GitHub.**

---

 Docker

The backend can be packaged into a Docker image.

Build the image:

```bash
docker build -t mentormatch .
```

Run the backend:

```bash
docker run --env-file .env -p 8000:8000 mentormatch
```

The project also uses Docker Compose to run the backend and PostgreSQL together.

```bash
docker compose up --build
```

Architecture:

```text
Docker Compose
│
├── FastAPI Container
│
└── PostgreSQL Container
```

---

 Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/Pravallika-puppala/MentorMatch.git
```

```bash
cd MentorMatch
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key

POSTGRES_HOST=localhost
POSTGRES_DB=mentormatch
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_PORT=5432
```

Never commit `.env`.

---

## 5. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Open the frontend

Run the frontend using VS Code Live Server or another static server.

The frontend communicates with the FastAPI backend through REST APIs.

---

 Running with Docker Compose

Make sure Docker Desktop is running.

Then:

```bash
docker compose up --build
```

The services include:

```text
FastAPI
PostgreSQL
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

Frontend

The frontend was intentionally built without React.

It uses:

* HTML
* CSS
* Vanilla JavaScript

The interface includes:

* Landing page
* Student profile form
* Mentor recommendation cards
* Match percentages
* "Why this mentor?" explanations
* Mentor detail modal
* AI Companion popup

The design follows a retro-futuristic startup aesthetic with a warm cream background and pastel technology-inspired accents.

---

 Testing

The application can be tested through FastAPI Swagger:

```text
http://127.0.0.1:8000/docs
```

Important flows:

### Student creation

```text
POST /students
```

### Mentor recommendation

```text
GET /students/{student_id}/recommendations
```

### AI Companion

```text
POST /students/{student_id}/companion
```

The full application flow can also be tested directly through the frontend.

---

Current Limitations

MentorMatch is currently an MVP.

Current limitations include:

* Training data is synthetic.
* Recommendation labels are generated from predefined compatibility rules.
* Real mentorship outcomes are not yet used for model training.
* Authentication is not implemented.
* Mentorship scheduling is not implemented.
* Messaging between students and mentors is not implemented.
* The recommendation model is an initial ML baseline rather than a production-scale ranking model.

These features could be introduced after collecting real platform interaction data.

---

Future Improvements

Potential future improvements include:

* Real mentorship feedback collection
* Learning-to-rank recommendation models
* Recommendation personalization from user behavior
* Mentor availability management
* Authentication and authorization
* Mentor-student messaging
* Mentorship scheduling
* Recommendation analytics
* Model monitoring
* A/B testing recommendation strategies
* Better evaluation using real mentorship outcomes

---

 What I Learned Building MentorMatch

This project brought together multiple parts of an end-to-end AI application:

* Designing REST APIs with FastAPI
* Working with PostgreSQL
* Connecting Python applications to databases
* Feature engineering for recommendation problems
* Training and loading ML models
* Building explainable recommendation outputs
* Integrating an LLM into an application
* Implementing controlled AI tools
* Connecting frontend and backend APIs
* Managing environment variables and secrets
* Containerizing applications with Docker
* Running multi-service applications with Docker Compose
* Debugging application and container networking
* Using Git and GitHub for version control

---

