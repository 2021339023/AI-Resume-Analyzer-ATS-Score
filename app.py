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
# Extract the resume's own "Skills" section
# ------------------------

SECTION_HEADINGS = [
    "experience",
    "work experience",
    "employment",
    "education",
    "projects",
    "certifications",
    "certificates",
    "summary",
    "objective",
    "achievements",
    "languages",
    "interests",
    "hobbies",
    "references",
    "awards",
    "publications",
    "training",
    "profile",
    "contact",
    "personal information",
    "declaration"
]


def extract_resume_skill_section(text):
    lines = text.split("\n")

    skill_lines = []
    inside_skills = False

    for line in lines:

        line_clean = line.strip()
        line_lower = line_clean.lower().strip(":.- ")

        # Detect the start of a "Skills" heading
        if not inside_skills:

            if "skill" in line_lower and len(line_lower.split()) <= 4:

                inside_skills = True

                # Example:
                # Skills: Python, SQL, Machine Learning
                if ":" in line_clean:

                    after_colon = line_clean.split(
                        ":", 1
                    )[1].strip()

                    if after_colon:
                        skill_lines.append(after_colon)

            continue


        # Stop when the next section heading is found
        if any(
            line_lower == h or line_lower.startswith(h)
            for h in SECTION_HEADINGS
        ):

            inside_skills = False
            continue


        if line_clean:
            skill_lines.append(line_clean)


    # Join all collected skill lines
    raw_block = " ".join(skill_lines)


    # Split skills using common separators
    items = re.split(
        r"[,|•▪·]|(?:\s-\s)|\n|;",
        raw_block
    )


    items = [
        i.strip(" .-\t")
        for i in items
        if i.strip(" .-\t")
    ]


    # Remove duplicates while keeping order
    seen = set()
    result = []

    for item in items:

        key = item.lower()

        if key not in seen:

            seen.add(key)
            result.append(item.title())


    return result


# ------------------------
# Matcher
# Checks ANY user-entered skill
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

        escaped = re.escape(skill_lower)


        # Word boundaries only where the skill
        # starts/ends with a word character
        #
        # Handles:
        # C++
        # Node.js
        # CI/CD
        # Python
        # SQL

        left = (
            r'\b'
            if skill_lower[0].isalnum()
            else ''
        )

        right = (
            r'\b'
            if skill_lower[-1].isalnum()
            else ''
        )


        pattern = left + escaped + right


        if re.search(pattern, text_lower):

            matched.append(
                skill_clean.title()
            )

        else:

            not_matched.append(
                skill_clean.title()
            )


    return matched, not_matched


# ------------------------
# Streamlit UI
# ------------------------

st.title(
    "AI Resume Skill Match Score & Analyzer"
)

st.subheader(
    "Enter Any Skill — Fully Custom, No Fixed Skill List"
)


# Required skills input
required_skills_input = st.text_area(
    "Enter Required Skills (comma-separated):",
    placeholder=(
        "e.g., Python, WordPress, PHP, "
        "Communication, Docker"
    )
)


# Resume upload
uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


# Analyze button
if st.button("Analyze"):

    if uploaded_resume and required_skills_input:

        # Convert required skills into a list
        required_skills = [
            skill.strip()
            for skill in required_skills_input.split(",")
            if skill.strip()
        ]


        # Extract resume text
        resume_text = extract_text_from_pdf(
            uploaded_resume
        )


        # 1. Extract skills from resume's own Skills section
        resume_skills = extract_resume_skill_section(
            resume_text
        )


        # 2. Match company's required skills
        # against the full resume text
        matched_skills, missing_skills = (
            match_required_skills(
                required_skills,
                resume_text
            )
        )


        # Calculate score
        score = (
            round(
                (
                    len(matched_skills)
                    / len(required_skills)
                ) * 100,
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
        # Skills Found in Resume
        # ------------------------

        st.write(
            "### Skills Found in Resume:"
        )


        if resume_skills:

            for skill in resume_skills:

                st.markdown(
                    f"- {skill}"
                )

        else:

            st.warning(
                "Couldn't detect a clear "
                "'Skills' section in this resume."
            )


        # ------------------------
        # Matched Skills
        # ------------------------

        st.write(
            "### Matched Skills "
            "(from your required list):"
        )


        if matched_skills:

            for skill in matched_skills:

                st.markdown(
                    f"- {skill}"
                )

        else:

            st.info(
                "None of your entered skills "
                "were found in the resume."
            )


        # ------------------------
        # Missing Skills
        # ------------------------

        st.write(
            "### Missing Skills "
            "(from your required list):"
        )


        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f"- {skill}"
                )

        else:

            st.success(
                "All entered skills were "
                "found in the resume!"
            )


    else:

        st.error(
            "Please provide the required skills "
            "and upload a resume PDF first!"
        )
