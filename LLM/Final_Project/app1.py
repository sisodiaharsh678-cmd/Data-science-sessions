import streamlit as st
from pypdf import PdfReader
import requests
import json
import re

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="<^>",
    layout="wide"
)

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

# TITLE
st.title("<^> AI Resume Analyzer")
st.write(
    """
    Upload your resume and paste a job description.
    The local LLM will analyze your resume against the job requirements."""
)

# SIDEBAR
with st.sidebar:
    st.header("## Configuration")
    st.write(f"**Model:** `{MODEL_NAME}`")
    st.write("**LLM:** Ollama")
    st.write("**Mode:** Local / Offline")
    st.divider()
    st.info(
        """
        This application uses a local LLM.
        
        Your resume is processed locally
        through Ollama rather than being sent
        to an external AI API.
        """
    )

# PDF TEXT EXTRACTION
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
            text += "\n"
    return text

# OLLAMA FUNCTION
def ask_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()
    data = response.json()
    return data["response"]

# CLEAN JSON
def clean_json_response(response):
    response = response.strip()
    # Remove ```json
    response = re.sub(
        r"```json",
        "",
        response,
        flags=re.IGNORECASE
    )

    # Remove ```
    response = response.replace(
        "```",
        ""
    )
    return response.strip()

# RESUME ANALYSIS
def analyze_resume(
    resume_text,
    job_description):
    prompt = f"""
You are an AI Resume Analysis Assistant.
Your task is to analyze a resume against a
job description.
IMPORTANT RULES:
1. Use only information present in the resume.
2. Do not invent candidate information.
3. If information is unavailable, use "Not mentioned".
4. Compare the resume skills with the job description.
5. Return ONLY valid JSON.
6. Do not use Markdown.
7. Do not include explanations outside JSON.

RESUME:
{resume_text}
JOB DESCRIPTION:
{job_description}

Return JSON using exactly this structure:
{{
    "candidate_name": "",
    "email": "",
    "phone": "",
    "education": [],
    "experience": [],
    "skills": [],
    "projects": [],
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "improvement_suggestions": [],
    "interview_questions": [],
    "professional_summary": ""
}}
"""
    return ask_ollama(prompt)

# INPUT SECTION
col1, col2 = st.columns(2)
# RESUME UPLOAD
with col1:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"]
    )

# JOB DESCRIPTION
with col2:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="""
Example:
We are looking for a Data Analyst
with knowledge of Python, SQL,
Power BI, Excel and statistics.
"""
    )

# ANALYZE BUTTON
if st.button(
    "Analyze Resume",
    type="primary"):

    # VALIDATION
    if uploaded_file is None:
        st.warning(
            "Please upload a resume PDF."
        )
        st.stop()
    if not job_description.strip():
        st.warning(
            "Please enter a job description."
        )
        st.stop()

    # EXTRACT TEXT
    with st.spinner(
        "Extracting resume text..."):
        resume_text = extract_text_from_pdf(
            uploaded_file
        )
    if not resume_text.strip():
        st.error(
            "Could not extract text from this PDF."
        )
        st.stop()

    # SHOW TEXT
    with st.expander(
        "View Extracted Resume Text"):
        st.text(resume_text)

    # CALL OLLAMA
    with st.spinner(
        "Ollama is analyzing the resume..."):
        try:
            result = analyze_resume(
                resume_text,
                job_description
            )
        except requests.exceptions.ConnectionError:
            st.error(
                """
                Could not connect to Ollama.
                Make sure Ollama is installed
                and running.
                Try:
                ollama serve
                """
            )
            st.stop()

        except Exception as e:
            st.error(
                f"Error: {e}"
            )
            st.stop()

    # CLEAN RESPONSE
    cleaned_result = clean_json_response(
        result
    )

    # CONVERT TO JSON
    try:
        analysis = json.loads(
            cleaned_result
        )
    except json.JSONDecodeError:
        st.error(
            "The model did not return valid JSON."
        )
        st.subheader(
            "Raw Model Response"
        )
        st.code(result)
        st.stop()

    # RESULTS
    st.divider()
    st.header(
        "Resume Analysis"
    )

    # CANDIDATE INFORMATION
    st.subheader(
        "Candidate Information"
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Candidate",
            analysis.get(
                "candidate_name",
                "Not mentioned"
            )
        )
    with col2:
        st.write("Email")
        st.write(
            analysis.get(
                "email",
                "Not mentioned"
            )
        )

    with col3:
        st.write("Phone")
        st.write(
            analysis.get(
                "phone",
                "Not mentioned"
            )
        )

    # EDUCATION
    st.subheader(
        "Education"
    )

    education = analysis.get(
        "education",
        []
    )

    if education:
        for item in education:
            st.write(
                f"• {item}"
            )
    else:
        st.write(
            "Not mentioned"
        )

    # EXPERIENCE
    st.subheader(
        "Experience"
    )

    experience = analysis.get(
        "experience",
        []
    )

    if experience:
        for item in experience:
            st.write(
                f"• {item}"
            )

    else:
        st.write(
            "Not mentioned"
        )

    # SKILLS
    st.subheader(
        "Skills"
    )

    skills = analysis.get(
        "skills",
        []
    )

    if skills:
        cols = st.columns(4)
        for i, skill in enumerate(skills):
            cols[i % 4].success(
                skill
            )
    else:
        st.write(
            "No skills identified."
        )

    # PROJECTS
    st.subheader(
        "Projects"
    )

    projects = analysis.get(
        "projects",
        []
    )

    for project in projects:
        st.write(
            f"• {project}"
        )

    # MATCHING SKILLS
    st.subheader(
        "Matching Skills"
    )

    matching = analysis.get(
        "matching_skills",
        []
    )

    if matching:
        for skill in matching:
            st.success(
                f"{skill}"
            )

    else:
        st.write(
            "No matching skills identified."
        )

    # MISSING SKILLS
    st.subheader(
        "Missing Skills"
    )

    missing = analysis.get(
        "missing_skills",
        []
    )

    if missing:
        for skill in missing:
            st.warning(
                f"• {skill}"
            )

    else:
        st.write(
            "No major missing skills identified."
        )

    # STRENGTHS
    st.subheader(
        "Strengths"
    )

    strengths = analysis.get(
        "strengths",
        []
    )

    for item in strengths:
        st.write(
            f"{item}"
        )

    # IMPROVEMENT SUGGESTIONS
    st.subheader(
        "Improvement Suggestions"
    )

    suggestions = analysis.get(
        "improvement_suggestions",
        []
    )

    for item in suggestions:
        st.info(
            item
        )

    # INTERVIEW QUESTIONS
    st.subheader(
        "Interview Questions"
    )

    questions = analysis.get(
        "interview_questions",
        []
    )

    for i, question in enumerate(
        questions,
        start=1):
        st.write(
            f"**{i}.** {question}"
        )

    # PROFESSIONAL SUMMARY
    st.subheader(
        "Professional Summary"
    )

    st.write(
        analysis.get(
            "professional_summary",
            "Not available"
        )
    )

    # DOWNLOAD
    json_output = json.dumps(
        analysis,
        indent=4
    )

    st.download_button(

        "Download Analysis",

        data=json_output,
        file_name="resume_analysis.json",
        mime="application/json"
    )

# FOOTER
st.divider()
st.caption(
    "AI Resume Analyzer | Python + Streamlit + Ollama + Llama"
)