import streamlit as st
import PyPDF2
import re

# ------------------------
# PDF Text Extract Function
# ------------------------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# ------------------------
# Automatic General Skill Extractor + Custom Pool Matcher
# ------------------------
def extract_all_resume_skills(text):
    # Common tech, business, and soft skills dictionary to automatically find general skills from the resume
    common_skill_pool = [
        "python", "java", "c++", "c#", "javascript", "typescript", "php", "ruby", "swift", "kotlin",
        "html", "css", "bootstrap", "tailwind", "react", "angular", "vue", "node.js", "django", "flask",
        "fastapi", "streamlit", "mysql", "postgresql", "mongodb", "sqlite", "sql", "oracle",
        "machine learning", "deep learning", "data science", "data analysis", "nlp", "computer vision",
        "tensorflow", "pytorch", "keras", "pandas", "numpy", "scikit-learn", "opencv",
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "linux", "ci/cd",
        "excel", "power bi", "tableau", "word", "powerpoint", "jira", "figma",
        "communication", "teamwork", "leadership", "problem solving", "time management", "project management"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skill_pool:
        # Use regex word boundaries to ensure exact keyword matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title())
            
    return list(set(found_skills))

# ------------------------
# Streamlit UI
# ------------------------
st.title("AI Resume Skill Match Score & Analyzer")
st.subheader("Dynamic Skill Extraction and Custom Job Requirement Matching")

# Company / User required skills input field (Completely non-predefined, user types whatever they want)
required_skills_input = st.text_area(
    "Enter Required Skills (comma-separated):",
    placeholder="e.g., Python, WordPress, PHP, Communication, Docker"
)

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

if st.button("Analyze"):
    if uploaded_resume and required_skills_input:
        # Parse user-defined required skills
        required_skills = [skill.strip().title() for skill in required_skills_input.split(",") if skill.strip()]
        
        # Extract raw text from the uploaded PDF resume
        resume_text = extract_text_from_pdf(uploaded_resume)
        
        # 1. Automatically find all general skills present in the resume text
        all_found_skills = extract_all_resume_skills(resume_text)
        
        # 2. Match user's required skills with the skills found in the resume (case-insensitive comparison)
        resume_skills_lower = {s.lower() for s in all_found_skills}
        matched_skills = [req for req in required_skills if req.lower() in resume_skills_lower]
        
        # 3. Calculate percentage score based on user-defined requirements
        if required_skills:
            score = round((len(matched_skills) / len(required_skills)) * 100, 2)
        else:
            score = 0.0

        st.success(f"Skill Match Score: {score} %")

        # Display All General Skills Found in Resume
        st.write("### Skills Found in Resume:")
        if all_found_skills:
            for skill in all_found_skills:
                st.markdown(f"- {skill}")
        else:
            st.warning("No standard skill keywords were automatically recognized in the resume text.")

        # Display Matched Required Skills against User's Input
        st.write("### Matched Required Skills:")
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"- {skill}")
        else:
            st.info("None of your entered required skills matched the resume content.")
            
    else:
        st.error("Please provide the required skills and upload a resume PDF first!")
