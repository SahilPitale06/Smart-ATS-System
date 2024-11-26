import base64
import io
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image
from PyPDF2 import PdfReader
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
from email.mime.text import MIMEText
import smtplib

# Set page configuration
st.set_page_config(page_title="Smart ATS", page_icon="📄", layout="wide")

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["End-User Side", "Admin Side"])

# Global text size increase
st.markdown(
    """
    <style>
    body {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to generate response using Generative AI
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to process PDF content for AI evaluation
def input_pdf_setup(uploaded_file, mode="image"):
    if mode == "image":  # End-User uses PDF-to-image approach
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        return [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
    elif mode == "text":  # Admin uses PDF-to-text approach
        reader = PdfReader(uploaded_file)
        text_content = "".join(page.extract_text() or "" for page in reader.pages)
        return [{"mime_type": "text/plain", "data": base64.b64encode(text_content.encode()).decode()}]

# End-User Side
if page == "End-User Side":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Smart Resume Evaluator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #808080;'>Evaluate your resume against job descriptions using AI</p>", unsafe_allow_html=True)

    # Job Description input
    st.subheader("📝 Job Description")
    input_text = st.text_area("Enter the Job Description:", placeholder="Paste job description here...")

    # File uploader
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF format)", type=["pdf"])
    if uploaded_file:
        st.success("PDF Uploaded Successfully")

    # Prompts for AI evaluation
    prompts = {
        "Tell Me About the Resume": """
            You are an experienced Technical Human Resource Manager, tasked with reviewing the provided resume against the job description. 
            Please share your professional evaluation on whether the candidate's profile aligns with the role, highlighting strengths and weaknesses.
        """,
        "Percentage Match": """
            As an ATS (Applicant Tracking System) scanner skilled in data science and ATS functionality, evaluate the resume for a match 
            percentage against the job description. First, provide the percentage match, then list missing keywords, and give final thoughts.
        """,
        "Skills to be Learned": """
            Evaluate the resume and identify skills the candidate is missing based on the job description. 
            Suggest the most important skills to learn to be a better match.
        """,
        "Experience Level Match": """
            Based on the job description, evaluate whether the candidate's experience level aligns with the position. 
            Provide insights on experience requirements (entry, mid, senior).
        """
    }

    # Buttons for actions
    st.markdown("<h2 style='color: #4CAF50;'>Choose Evaluation Option</h2>", unsafe_allow_html=True)
    options = list(prompts.keys())
    selected_option = st.radio("Evaluation Type", options, horizontal=True)

    # Displaying the AI response
    if st.button("Evaluate"):
        if uploaded_file:
            try:
                pdf_content = input_pdf_setup(uploaded_file, mode="image")
                response = get_gemini_response(input_text, pdf_content, prompts[selected_option])
                st.markdown(f"<h3 style='color: #4CAF50;'>{selected_option} Result</h3>", unsafe_allow_html=True)
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload the resume.")

# Admin Side
# Admin Side
elif page == "Admin Side":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Employer ATS System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #808080;'>Rank resumes by relevancy and analyze skill gaps using AI</p>", unsafe_allow_html=True)

    # Job Description input
    st.subheader("📝 Job Description")
    input_text = st.text_area("Enter the Job Description:", placeholder="Paste job description here...")

    # File uploader for bulk resumes
    uploaded_files = st.file_uploader("📄 Upload Resumes (PDF format)", type=["pdf"], accept_multiple_files=True)

    # Button to Rank Resumes
    if st.button("🔍 Rank Resumes by Relevancy"):
        if uploaded_files:
            resume_scores = []
            skills_data = []
            for file in uploaded_files:
                pdf_content = input_pdf_setup(file, mode="text")
                score_response = get_gemini_response(input_text, pdf_content, """
                    You are an ATS expert. Evaluate each resume in relation to the job description, 
                    and provide only a score as a percentage (e.g., "85%") indicating relevancy.
                """)
                skill_gap_response = get_gemini_response(input_text, pdf_content, """
                    As a career advisor, analyze the resumes for skill gaps in relation to the provided job description. 
                    For each resume, identify missing skills and recommend specific improvements.
                """)

                match = re.search(r"(\d+)%", score_response)
                score = int(match.group(1)) if match else 0
                resume_scores.append({"name": file.name, "score": score})
                skills_data.append({"name": file.name, "skills_missing": skill_gap_response})

            # Display Results
            st.markdown("<h3 style='color: #4CAF50;'>Resume Rankings Based on Relevancy</h3>", unsafe_allow_html=True)
            ranked_df = pd.DataFrame(resume_scores).sort_values(by="score", ascending=False)
            st.write(ranked_df)

            # Plot Rankings
            fig, ax = plt.subplots()
            sns.barplot(x="name", y="score", data=ranked_df, ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Relevancy Scores for Each Resume")
            st.pyplot(fig)

            # Skill Gaps
            st.markdown("<h3 style='color: #4CAF50;'>Skill Gaps in Resumes</h3>", unsafe_allow_html=True)
            skill_gap_df = pd.DataFrame(skills_data)
            st.write(skill_gap_df)

            # Email Notification for Candidates
            st.markdown("<h3 style='color: #4CAF50;'>Send Acceptance/Rejection Emails</h3>", unsafe_allow_html=True)
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
                        st.success(f"Email sent to {email} ({decision.capitalize()})")
                    except Exception as e:
                        st.error(f"Failed to send email to {email}: {e}")
        else:
            st.warning("Please upload resumes.")