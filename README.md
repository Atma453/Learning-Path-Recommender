# Learning-Path-Recommender
Developed an AI-powered educational agent using Retrieval-Augmented Generation (RAG) to compress real course catalogs and learner progress into personalized multi-week learning paths, adaptive quizzes, and career recommendations using Gemini LLM and vector databases.

# AI-Powered Learning Path Recommender using RAG

## Project Description

The AI-Powered Learning Path Recommender is an intelligent educational agent designed to compress course catalogs and student learning progress to generate personalized learning paths efficiently. 

The system ingests real IT course materials in PDF format, stores them in a vector database, and applies Retrieval-Augmented Generation (RAG) using a Large Language Model (Gemini) to retrieve relevant content. Based on learner progress (completed weeks), the AI dynamically generates a structured 12-week roadmap, adaptive quizzes, and career growth recommendations.

This project demonstrates how AI can automate curriculum design, personalize education, and provide intelligent mentorship without relying on static datasets.


## Key Features

- Automatic Course Catalog Ingestion (PDF-based)
- Retrieval-Augmented Generation (RAG) Architecture
- Structured 12-Week Learning Roadmap
- Student Progress Tracking
- Adaptive Weekly Quiz Generation
- AI-Based Career Growth Suggestions
- Personalized Learning Path Adjustment
- Automatic Catalog Loading (No Manual Setup Required)


## How It Works

1. Course PDFs are loaded and processed using PyPDF.
2. The extracted content is stored in ChromaDB (Vector Database).
3. When a user enters a skill, relevant content is retrieved using semantic search.
4. Gemini LLM generates:
   - A personalized 12-week roadmap
   - Weekly quizzes
   - Career guidance
5. Student progress is tracked and used to adapt future recommendations.


## System Architecture

User Input → Vector Retrieval (ChromaDB) → Gemini LLM →  
Personalized Roadmap + Quiz + Career Suggestions


## Technologies Used

- Python
- Streamlit (Frontend & UI)
- Gemini LLM (google-genai)
- ChromaDB (Vector Database)
- PyPDF (PDF Processing)
- Retrieval-Augmented Generation (RAG)

## How to Run Locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py
