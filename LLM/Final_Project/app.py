import streamlit as st
from pypdf import PdfReader
import requests
import json

st.title("<^> AI Resume Analyzer")

# Upload Resume
pdf = st.file_uploader("Upload Resume", type="pdf")

# Job Description
job = st.text_area("Enter Job Description")


# Read PDF
def read_pdf(pdf):
    reader = PdfReader(pdf)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# Analyze Resume
def analyze(resume, job):

    prompt = f"""
    Analyze this resume for the given job.

    Resume:
    {resume}

    Job:
    {job}

    Give:
    1. Matching Skills
    2. Missing Skills
    3. Strengths
    4. Suggestions
    5. Interview Questions
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


# Button
if st.button("Analyze"):
    if pdf and job:
        resume = read_pdf(pdf)
        with st.spinner("Analyzing..."):
            result = analyze(resume, job)
        st.subheader("Analysis")
        st.write(result)

    else:

        st.warning("Upload resume and enter job description.")