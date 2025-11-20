'''


import streamlit as st
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------
# PDF Text Extract Function
# ------------------------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# ------------------------
# Skill Extraction (Basic NLP)
# ------------------------
def extract_skills(text):
    skill_keywords = [
        "python", "c++", "machine learning", "deep learning",
        "excel", "power bi", "sql", "communication", "teamwork",
        "tensorflow", "pytorch", "data analysis", "data science",
        "streamlit", "aws", "docker", "nlp", "opencv"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills

# ------------------------
# Score Calculation
# ------------------------
def calculate_match_score(resume_text, job_desc):
    documents = [resume_text, job_desc]
    tfidf = TfidfVectorizer().fit_transform(documents)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)

# ------------------------
# Streamlit UI
# ------------------------
st.title("AI Resume Analyzer + ATS Score")
st.subheader("Upload your resume and job description to get score")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if uploaded_resume and job_description:
        resume_text = extract_text_from_pdf(uploaded_resume)
        skills = extract_skills(resume_text)
        score = calculate_match_score(resume_text, job_description)

        st.success(f"ATS Match Score: {score} %")

        st.write("### Extracted Skills:")
        st.write(skills)

    else:
        st.error("Please upload a resume and job description!")
'''


# app.py


import streamlit as st
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------
# PDF Text Extract Function
# ------------------------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# ------------------------
# Skill Extraction (Basic NLP)
# ------------------------
def extract_skills(text):
    skill_keywords = [
        "python", "java", "c++", "machine learning", "deep learning",
        "excel", "power bi", "sql", "communication", "teamwork",
        "tensorflow", "pytorch", "data analysis", "data science",
        "streamlit", "aws", "docker", "nlp", "opencv","php"," bootstrap-5"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills

# ------------------------
# Score Calculation (Resume vs Job Description)
# ------------------------
def calculate_match_score(resume_text, job_desc):
    documents = [resume_text, job_desc]
    tfidf = TfidfVectorizer().fit_transform(documents)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)

# ------------------------
# ------------------------
# Streamlit UI
# ------------------------
st.title("AI Resume Skill Match Score")
st.subheader("Upload your resume PDF to get skill match score")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

# Predefined required skills (example)
required_skills = [
    "python","java","php", "c++", "machine learning", "deep learning",
    "sql", "tensorflow", "pytorch", "docker", "nlp", "opencv"," bootstrap-5"
]

if st.button("Analyze"):
    if uploaded_resume:
        resume_text = extract_text_from_pdf(uploaded_resume)
        found_skills = extract_skills(resume_text)

        # Calculate skill match percentage
        matched = set(found_skills) & set(required_skills)
        score = round((len(matched) / len(required_skills)) * 100, 2)

        st.success(f"Skill Match Score: {score} %")
        st.write("### Skills Found in Resume:")
        st.write(found_skills)
        st.write("### Matched Required Skills:")
        st.write(list(matched))
    else:
        st.error("Please upload a resume PDF!")


