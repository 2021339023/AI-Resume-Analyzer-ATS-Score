import streamlit as st
import PyPDF2
import re

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="Resume Skill Matcher",
    page_icon="🧩",
    layout="centered"
)

# ------------------------
# Custom CSS Styling
# ------------------------
st.markdown("""
<style>
    .main {
        background-color: #f7f8fc;
    }

    .hero {
        background: linear-gradient(135deg, #6C63FF 0%, #4A47A3 100%);
        padding: 2.2rem 2rem;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 24px rgba(76, 71, 163, 0.25);
    }
    .hero h1 {
        color: white;
        font-size: 2rem;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #E5E3FF;
        font-size: 1rem;
        margin: 0;
    }

    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1.2rem;
        border: 1px solid #eef0f7;
    }

    .score-box {
        text-align: center;
        padding: 1.6rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(24, 90, 157, 0.25);
    }
    .score-box h2 {
        font-size: 2.6rem;
        margin: 0;
    }
    .score-box p {
        margin: 0;
        opacity: 0.9;
    }

    .skill-pill-matched {
        display: inline-block;
        background: #E6F9F0;
        color: #12805C;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px 6px 4px 0;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid #B7EEDA;
    }

    .skill-pill-missing {
        display: inline-block;
        background: #FDEDEE;
        color: #C0392B;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px 6px 4px 0;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid #F8CFD1;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6C63FF 0%, #4A47A3 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

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
# Hero Header
# ------------------------
st.markdown("""
<div class="hero">
    <h1>🧩 Resume Skill Matcher</h1>
    <p>Enter any required skills and instantly score a resume against them</p>
</div>
""", unsafe_allow_html=True)

# ------------------------
# Input Section
# ------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("#### 1️⃣ Required Skills")
required_skills_input = st.text_area(
    "Enter required skills, separated by commas",
    placeholder="e.g., Python, WordPress, PHP, Communication, Docker",
    label_visibility="collapsed"
)

st.markdown("#### 2️⃣ Upload Resume")
uploaded_resume = st.file_uploader("Upload a PDF resume", type=["pdf"], label_visibility="collapsed")

analyze_clicked = st.button("🔍 Analyze Resume")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------
# Results
# ------------------------
if analyze_clicked:
    if uploaded_resume and required_skills_input:
        required_skills = [skill.strip() for skill in required_skills_input.split(",") if skill.strip()]
        resume_text = extract_text_from_pdf(uploaded_resume)

        matched_skills, missing_skills = match_required_skills(required_skills, resume_text)
        score = round((len(matched_skills) / len(required_skills)) * 100, 2) if required_skills else 0.0

        st.markdown(f"""
        <div class="score-box">
            <h2>{score}%</h2>
            <p>Skill Match Score &nbsp;•&nbsp; {len(matched_skills)} of {len(required_skills)} skills matched</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(int(score), 100))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### ✅ Matched Skills")
            if matched_skills:
                pills = "".join(f'<span class="skill-pill-matched">{s}</span>' for s in matched_skills)
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.info("No matches found.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("#### ❌ Missing Skills")
            if missing_skills:
                pills = "".join(f'<span class="skill-pill-missing">{s}</span>' for s in missing_skills)
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.success("All required skills found!")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("⚠️ Please enter required skills and upload a resume PDF first.")
