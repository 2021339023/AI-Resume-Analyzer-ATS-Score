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
# Automatic General Skill Extractor (for the "Skills Found in Resume" overview)
# ------------------------
def extract_all_resume_skills(text):
    # Common tech, business, and soft skills dictionary — used only to SHOW a general
    # overview of well-known skills present in the resume. This list does NOT limit
    # what the company can require/match against (see match_required_skills below).
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
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title())

    return sorted(set(found_skills))


# ------------------------
# Direct Matcher: checks ANY company-entered skill against the resume text itself
# (not limited to the common_skill_pool above) — this is what fixes the matching.
# ------------------------
def match_required_skills(required_skills, resume_text):
    text_lower = resume_text.lower()
    matched = []

    for skill in required_skills:
        skill_clean = skill.strip()
        if not skill_clean:
            continue

        skill_lower = skill_clean.lower()

        # Build a safe regex pattern. Multi-word skills (e.g. "power bi") and
        # skills with special characters (e.g. "c++", "node.js", "ci/cd") are handled
        # by escaping first, then loosening the boundary rules a bit.
        escaped = re.escape(skill_lower)

        # Use word boundaries where the skill starts/ends with a word character;
        # otherwise (e.g. starts with a symbol like "++") just match the escaped text.
        left = r'\b' if skill_lower[0].isalnum() else ''
        right = r'\b' if skill_lower[-1].isalnum() else ''
        pattern = left + escaped + right

        if re.search(pattern, text_lower):
            matched.append(skill_clean.title())

    return matched


# ------------------------
# Streamlit UI
# ------------------------
st.title("AI Resume Skill Match Score & Analyzer")
st.subheader("Dynamic Skill Extraction and Custom Job Requirement Matching")

# Company / User required skills input field (Completely free text — any skill works)
required_skills_input = st.text_area(
    "Enter Required Skills (comma-separated):",
    placeholder="e.g., Python, WordPress, PHP, Communication, Docker"
)

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

if st.button("Analyze"):
    if uploaded_resume and required_skills_input:
        # Parse company's own free-text required skills (no predefined list restriction)
        required_skills = [skill.strip() for skill in required_skills_input.split(",") if skill.strip()]

        # Extract raw text from the uploaded PDF resume
        resume_text = extract_text_from_pdf(uploaded_resume)

        # 1. General overview: well-known skills automatically recognized in the resume
        all_found_skills = extract_all_resume_skills(resume_text)

        # 2. Real matching: check EACH company-entered skill directly against the resume
        #    text, regardless of whether it's in the common pool or not
        matched_skills = match_required_skills(required_skills, resume_text)

        # 3. Score based on how many of the company's required skills were matched
        if required_skills:
            score = round((len(matched_skills) / len(required_skills)) * 100, 2)
        else:
            score = 0.0

        st.success(f"Skill Match Score: {score} %")

        # Display All General Skills Found in Resume (overview only)
        st.write("### Skills Found in Resume:")
        if all_found_skills:
            for skill in all_found_skills:
                st.markdown(f"- {skill}")
        else:
            st.warning("No standard skill keywords were automatically recognized in the resume text.")

        # Display Matched Required Skills against the Company's Input
        st.write("### Matched Required Skills:")
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"- {skill}")
        else:
            st.info("None of your entered required skills matched the resume content.")

    else:
        st.error("Please provide the required skills and upload a resume PDF first!")
