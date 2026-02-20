import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb

# =====================
# SETUP
# =====================
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("courses")

COURSE_FOLDER = "courses"

# =====================
# SESSION MEMORY
# =====================
if "completed_weeks" not in st.session_state:
    st.session_state.completed_weeks = []

if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""

if "skill" not in st.session_state:
    st.session_state.skill = ""

# =====================
# PDF INGESTION
# =====================
def load_pdfs():
    texts = []
    for file in os.listdir(COURSE_FOLDER):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(COURSE_FOLDER, file))
            for page in reader.pages:
                if page.extract_text():
                    texts.append(page.extract_text())
    return texts

def store_courses():
    texts = load_pdfs()
    for i, t in enumerate(texts):
        collection.add(documents=[t], ids=[str(i)])

# =====================
# RAG RETRIEVAL
# =====================
def retrieve_context(query):
    results = collection.query(query_texts=[query], n_results=3)
    return " ".join(results["documents"][0])

# =====================
# AI GENERATION
# =====================
def generate_roadmap(skill):
    context = retrieve_context(skill)
    progress = ", ".join([f"Week {w}" for w in st.session_state.completed_weeks])

    prompt = f"""
You are an AI mentor.

Course content:
{context}

Student progress: {progress if progress else "None"}

Create a personalized 12-week roadmap for {skill}.
Adjust difficulty based on completed weeks.

For each week include:
- Topics
- Practical project
"""

    r = client.models.generate_content(model=MODEL, contents=prompt)
    return r.text


def generate_quiz(skill, week):
    prompt = f"""
Create a quiz for {skill} Week {week}.
5 MCQs + answers.
Difficulty should match student's progress.
"""
    r = client.models.generate_content(model=MODEL, contents=prompt)
    return r.text


def career_suggestions(skill):
    progress = st.session_state.completed_weeks

    prompt = f"""
Student is learning {skill}
Completed weeks: {progress}

Suggest:
- Career paths
- Industry tools
- Certifications
- Next advanced skills
"""

    r = client.models.generate_content(model=MODEL, contents=prompt)
    return r.text

# =====================
# UI
# =====================
st.title("🎓 Learning Path Recommender")

if st.button("📥 Load Course Catalog"):
    store_courses()
    st.success("Course PDFs loaded into AI memory!")

skill = st.text_input("Enter Skill")

if skill:
    st.session_state.skill = skill

if st.button("📅 Generate Personalized 12-Week Roadmap"):
    if skill:
        st.session_state.roadmap = generate_roadmap(skill)
        st.write(st.session_state.roadmap)

st.divider()

st.subheader("✅ Progress Tracker")

week_done = st.number_input("Mark completed week", 1, 12)

if st.button("Save Completed Week"):
    if week_done not in st.session_state.completed_weeks:
        st.session_state.completed_weeks.append(week_done)
        st.success(f"Week {week_done} completed!")

st.write("Completed Weeks:", st.session_state.completed_weeks)

st.divider()

st.subheader("📝 Weekly Quiz")

quiz_week = st.number_input("Select week for quiz", 1, 12)

if st.button("Generate Quiz"):
    if st.session_state.skill:
        quiz = generate_quiz(st.session_state.skill, quiz_week)
        st.write(quiz)

st.divider()

st.subheader("🚀 AI Career Growth Suggestions")

if st.button("Get Career Advice"):
    advice = career_suggestions(st.session_state.skill)
    st.write(advice)