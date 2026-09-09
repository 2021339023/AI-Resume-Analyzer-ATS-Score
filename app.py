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
# Matcher: checks ANY user-entered skill
# against the resume text
# ------------------------
def match_required_skills(required_skills, resume_text):
    text_lower = resume_text.lower()

    matched = []
    not_matched = []

    for skill in required_skills:
        skill_clean = skill.strip()

        if not skill_clean:
            continue

        skill_lower = skill_clean.lower()

        # Escape special characters
        # Handles things like:
        # C++, Node.js, CI/CD
        escaped = re.escape(skill_lower)

        # Use word boundaries where appropriate
        left = r'\b' if skill_lower[0].isalnum() else ''
        right = r'\b' if skill_lower[-1].isalnum() else ''

        pattern = left + escaped + right

        if re.search(pattern, text_lower):
            matched.append(skill_clean.title())
        else:
            not_matched.append(skill_clean.title())

    return matched, not_matched


# ------------------------
# Streamlit UI
# ------------------------
st.title("AI Resume Skill Match Score & Analyzer")

st.subheader(
    "Enter Any Skill — Fully Custom, No Fixed Skill List"
)


# Company / User required skills input field
required_skills_input = st.text_area(
    "Enter Required Skills (comma-separated):",
    placeholder="e.g., Python, WordPress, PHP, Communication, Docker"
)


# Resume upload
uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


# Analyze button
if st.button("Analyze"):

    if uploaded_resume and required_skills_input:

        # Parse the company's free-text required skills
        required_skills = [
            skill.strip()
            for skill in required_skills_input.split(",")
            if skill.strip()
        ]

        # Extract raw text from uploaded PDF
        resume_text = extract_text_from_pdf(
            uploaded_resume
        )

        # Check each entered skill against resume
        matched_skills, missing_skills = match_required_skills(
            required_skills,
            resume_text
        )

        # Calculate skill match score
        score = (
            round(
                (len(matched_skills) / len(required_skills)) * 100,
                2
            )
            if required_skills
            else 0.0
        )

        # Display score
        st.success(
            f"Skill Match Score: {score} %"
        )


        # ------------------------
        # Matched Skills
        # ------------------------
        st.write(
            "### Matched Skills (Found in Resume):"
        )

        if matched_skills:

            for skill in matched_skills:
                st.markdown(f"- {skill}")

        else:
            st.info(
                "None of your entered skills were found in the resume."
            )


        # ------------------------
        # Missing Skills
        # ------------------------
        st.write(
            "### Missing Skills (Not Found in Resume):"
        )

        if missing_skills:

            for skill in missing_skills:
                st.markdown(f"- {skill}")

        else:
            st.success(
                "All entered skills were found in the resume!"
            )

    else:

        st.error(
            "Please provide the required skills and upload a resume PDF first!"
        )
