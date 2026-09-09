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
# Extract the resume's own "Skills" section (no predefined dictionary at all).
# PDF text extraction often loses line/column structure, so instead of relying on
# line-by-line parsing, we search the whole text for a "skills" heading and the
# next likely section heading, then clean up whatever falls between them.
# ------------------------
SECTION_HEADINGS = [
    "experience", "work experience", "employment", "education", "projects",
    "certifications", "certificates", "summary", "objective", "achievements",
    "languages", "interests", "hobbies", "references", "awards", "publications",
    "training", "profile", "contact", "personal information", "declaration",
    "about me", "about"
]

MAX_SKILL_WORDS = 4  # a real skill/phrase is short; longer chunks are sentences, not skills

def extract_resume_skill_section(text):
    text_norm = re.sub(r"\s+", " ", text)  # collapse broken line breaks/whitespace
    lower = text_norm.lower()

    # Find where a "skills" heading starts (word boundary so it doesn't match mid-word)
    heading_match = re.search(r"\bskills?\b", lower)
    if not heading_match:
        return []

    start = heading_match.end()

    # Find the nearest following section heading to know where "skills" content ends
    end = len(text_norm)
    for heading in SECTION_HEADINGS:
        m = re.search(r"\b" + re.escape(heading) + r"\b", lower[start:])
        if m:
            end = min(end, start + m.start())

    block = text_norm[start:end]

    # Split into individual items on common separators
    items = re.split(r"[,|•▪·;/]|(?:\s-\s)", block)
    items = [i.strip(" .-:\t") for i in items if i.strip(" .-:\t")]

    # Keep only short, skill-like phrases; drop long sentence fragments
    cleaned = []
    seen = set()
    for item in items:
        word_count = len(item.split())
        if 0 < word_count <= MAX_SKILL_WORDS:
            key = item.lower()
            if key not in seen:
                seen.add(key)
                cleaned.append(item.title())

    return cleaned


# ------------------------
# Matcher: checks ANY user-entered skill (no predefined list) against the resume text
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
        escaped = re.escape(skill_lower)

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
st.subheader("Enter Any Skill — Fully Custom, No Fixed Skill List")

required_skills_input = st.text_area(
    "Enter Required Skills (comma-separated):",
    placeholder="e.g., Python, WordPress, PHP, Communication, Docker"
)

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

if st.button("Analyze"):
    if uploaded_resume and required_skills_input:
        required_skills = [skill.strip() for skill in required_skills_input.split(",") if skill.strip()]
        resume_text = extract_text_from_pdf(uploaded_resume)

        resume_skills = extract_resume_skill_section(resume_text)
        matched_skills, missing_skills = match_required_skills(required_skills, resume_text)

        score = round((len(matched_skills) / len(required_skills)) * 100, 2) if required_skills else 0.0

        st.success(f"Skill Match Score: {score} %")

        st.write("### Skills Found in Resume:")
        if resume_skills:
            for skill in resume_skills:
                st.markdown(f"- {skill}")
        else:
            st.warning("Couldn't detect a clear 'Skills' section in this resume.")

        st.write("### Matched Skills (from your required list):")
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"- {skill}")
        else:
            st.info("None of your entered skills were found in the resume.")

        st.write("### Missing Skills (from your required list):")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- {skill}")
        else:
            st.success("All entered skills were found in the resume!")

    else:
        st.error("Please provide the required skills and upload a resume PDF first!")
