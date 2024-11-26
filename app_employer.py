from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PyPDF2 import PdfReader
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
from email.mime.text import MIMEText
import smtplib

# Load environment variables
load_dotenv()

# Set up Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    # Convert PDF to text using PyPDF2
    reader = PdfReader(uploaded_file)
    text_content = ""

    for page in reader.pages:
        text_content += page.extract_text() or ""  # Extract text from each page
    
    pdf_parts = [
        {
            "mime_type": "text/plain",
            "data": base64.b64encode(text_content.encode()).decode()
        }
    ]
    return pdf_parts

# Configure the Streamlit app
st.set_page_config(page_title="Employer ATS Resume Expert")
st.header("Employer ATS System")

# Job Description Input
input_text = st.text_area("Job Description: ", key="input")

# Upload Resumes in Bulk
uploaded_files = st.file_uploader("Upload Resumes (PDFs)...", type=["pdf"], accept_multiple_files=True)

# Button to Rank Resumes
rank_resumes = st.button("Rank Resumes by Relevancy")

# Prompts for Ranking and Skill Gap Analysis
ranking_prompt = """
You are an ATS (Applicant Tracking System) expert. Evaluate each resume in relation to the given job description, 
and provide only a score as a percentage (e.g., "85%") indicating the relevancy of each resume to the job role.
"""

skill_gap_prompt = """
As a career advisor, analyze the resumes for skill gaps in relation to the provided job description. 
For each resume, identify missing skills and recommend specific improvements or areas of focus for the candidates.
"""

# Lists to hold the data for ranking and skill analysis
resume_scores = []
skills_data = []

if rank_resumes and uploaded_files:
    for file in uploaded_files:
        # Process each resume
        pdf_content = input_pdf_setup(file)
        
        # Get the ranking and skill gap response for each resume
        score_response = get_gemini_response(input_text, pdf_content, ranking_prompt)
        skill_gap_response = get_gemini_response(input_text, pdf_content, skill_gap_prompt)
        
        # Extract the score using a regular expression
        match = re.search(r"(\d+)%", score_response)
        if match:
            score = int(match.group(1))
        else:
            score = 0  # Default score if no percentage is found
        resume_scores.append({"name": file.name, "score": score})
        
        # Collect skill gap data
        skills_data.append({"name": file.name, "skills_missing": skill_gap_response})
    
    # Display Ranking Results
    st.subheader("Resume Rankings Based on Relevancy")
    ranked_df = pd.DataFrame(resume_scores).sort_values(by="score", ascending=False)
    st.write(ranked_df)
    
    # Plot Ranking Scores
    fig, ax = plt.subplots()
    sns.barplot(x="name", y="score", data=ranked_df, ax=ax)
    plt.xticks(rotation=45)
    ax.set_title("Relevancy Scores for Each Resume")
    st.pyplot(fig)

    # Display Skill Gap Data
    st.subheader("Skill Gaps in Resumes")
    skill_gap_df = pd.DataFrame(skills_data)
    st.write(skill_gap_df)

    # Plot Missing Skills by Resume (Assuming text parsing for missing skills in the response)
    missing_skills_summary = {
        "Resume": [],
        "Missing Skills": []
    }
    
    for row in skills_data:
        resume_name = row["name"]
        skills = row["skills_missing"]
        missing_skills_summary["Resume"].append(resume_name)
        missing_skills_summary["Missing Skills"].append(len(skills.split(',')))
    
    missing_skills_df = pd.DataFrame(missing_skills_summary)
    fig2, ax2 = plt.subplots()
    sns.barplot(x="Resume", y="Missing Skills", data=missing_skills_df, ax=ax2)
    plt.xticks(rotation=45)
    ax2.set_title("Number of Missing Skills by Resume")
    st.pyplot(fig2)

    # Email Notification for Candidates
    st.subheader("Send Acceptance/Rejection Emails")
    st.write("Enter the email addresses of candidates to send acceptance/rejection notifications based on relevancy scores.")
    
    for index, row in ranked_df.iterrows():
        email = st.text_input(f"Email for {row['name']} (Score: {row['score']}%)", key=row['name'])
        accept = st.button(f"Send Acceptance to {row['name']}", key=f"accept_{row['name']}")
        reject = st.button(f"Send Rejection to {row['name']}", key=f"reject_{row['name']}")

        if accept or reject:
            decision = "accepted" if accept else "rejected"
            subject = f"Job Application {decision.capitalize()}"
            message_body = f"Dear Candidate,\n\nYour application has been {decision} for the specified job position based on our resume analysis.\n\nBest Regards,\nEmployer"
            message = MIMEText(message_body)
            message["Subject"] = subject
            message["From"] = os.getenv("EMAIL_ADDRESS")
            message["To"] = email
            
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
                    server.sendmail(os.getenv("EMAIL_ADDRESS"), email, message.as_string())
                st.write(f"Email sent to {email} ({decision.capitalize()})")
            except Exception as e:
                st.write(f"Failed to send email to {email}: {e}")





# # conda -p venv python==3.10 -y