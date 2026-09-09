import streamlit as st
import PyPDF2

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
# Skill Extraction (Basic NLP)
# ------------------------
def extract_skills(text):
    skill_keywords = [
        "python", "java", "php", "c++", "machine learning", "deep learning",
        "excel", "power bi", "sql", "communication", "teamwork",
        "tensorflow", "pytorch", "data analysis", "data science",
        "streamlit", "aws", "docker", "nlp", "opencv", "bootstrap-5"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills

# ------------------------
# Streamlit UI
# ------------------------
st.title("AI Resume Skill Match Score")
st.subheader("Upload your resume PDF to get skill match score")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

# Predefined required skills
required_skills = [
    "python", "java", "php", "c++", "machine learning", "deep learning",
    "sql", "tensorflow", "pytorch", "docker", "nlp", "opencv", "bootstrap-5"
]

if st.button("Analyze"):
    if uploaded_resume:
        resume_text = extract_text_from_pdf(uploaded_resume)
        found_skills = extract_skills(resume_text)

        # Calculate skill match percentage
        matched = set(found_skills) & set(required_skills)
        score = round((len(matched) / len(required_skills)) * 100, 2) if required_skills else 0.0

        st.success(f"Skill Match Score: {score} %")

        # Display Skills Found in Resume using clean bullet points
        st.write("### Skills Found in Resume:")
        if found_skills:
            for skill in found_skills:
                st.markdown(f"- {skill.title()}")
        else:
            st.info("No matching skills found in the resume.")

        # Display Matched Required Skills using clean bullet points
        st.write("### Matched Required Skills:")
        if matched:
            for skill in matched:
                st.markdown(f"- {skill.title()}")
        else:
            st.info("No required skills matched.")
            
    else:
      st.error("Please upload a resume PDF!")
