# from dotenv import load_dotenv

# load_dotenv()
# import base64
# import streamlit as st
# import os
# import io
# from PIL import Image 
# import pdf2image
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,pdf_cotent,prompt):
#     model=genai.GenerativeModel('gemini-1.5-flash')
#     response=model.generate_content([input,pdf_content[0],prompt])
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         ## Convert the PDF to image
#         images=pdf2image.convert_from_bytes(uploaded_file.read())

#         first_page=images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume EXpert")
# st.header("ATS Tracking System")
# input_text=st.text_area("Job Description: ",key="input")
# uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")


# submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

# submit3 = st.button("Percentage match")

# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """
# input_prompt2 = """
# You are an experienced career coach with expertise in identifying skill gaps and providing actionable guidance for career development. 
# Based on the candidate's resume and the job description provided, please identify areas where the candidate can improve their skills.
# Provide concrete recommendations for each skill gap, suggest resources, courses, or certifications if applicable, and 
# highlight any emerging industry trends or skills that would strengthen the candidate's profile for the targeted role.
# """

# input_prompt3 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt1,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")
# elif submit2:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt2,pdf_content,input_text)
#         st.subheader("Skill Improvement Suggestions")
#         st.write(response)
#     else:
#         st.write("Please upload the resume")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt3,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")



import base64
import io
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image    
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate response using the generative model
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to set up and process PDF content
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image (first page)
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes and base64 encode
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

    

# Streamlit app layout
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Smart Resume Evaluator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #808080;'>Evaluate your resume against job descriptions using AI</p>", unsafe_allow_html=True)

# Job Description input
st.subheader("📝 Job Description")
input_text = st.text_area("Enter the Job Description:", key="input", placeholder="Paste job description here...")

# File uploader
uploaded_file = st.file_uploader("📄 Upload your resume (PDF format)", type=["pdf"])
if uploaded_file:
    st.success("PDF Uploaded Successfully")

# Prompts for AI evaluation
input_prompt1 = """
You are an experienced Technical Human Resource Manager, tasked with reviewing the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role, highlighting strengths and weaknesses.
"""

input_prompt3 = """
As an ATS (Applicant Tracking System) scanner skilled in data science and ATS functionality, evaluate the resume for a match 
percentage against the job description. First, provide the percentage match, then list missing keywords, and give final thoughts.
"""
input_prompt2 = """
Evaluate the resume and identify skills the candidate is missing based on the job description. 
Suggest the most important skills to learn to be a better match.
"""

input_prompt4 = """
Based on the job description, evaluate whether the candidate's experience level aligns with the position. 
Provide insights on experience requirements (entry, mid, senior).
"""

# Buttons for actions
st.markdown("<h2 style='color: #4CAF50;'>Choose Evaluation Option</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    submit1 = st.button("Tell Me About the Resume")
with col2:
    submit3 = st.button("Percentage Match")
with col3:
    submit2 = st.button("Skills to be Learned")
with col1:
    submit4 = st.button("Experience Level Match")

# Displaying the AI response
if submit1:
    if uploaded_file:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.markdown("<h3 style='color: #4CAF50;'>AI Evaluation Result</h3>", unsafe_allow_html=True)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload the resume.")

elif submit3:
    if uploaded_file:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.markdown("<h3 style='color: #4CAF50;'>Percentage Match Result</h3>", unsafe_allow_html=True)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload the resume.")

elif submit2:
    if uploaded_file:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
            visualizations = False  # You can disable visualizations if not needed
            st.markdown("<h3 style='color: #4CAF50;'>Skills to be Learned</h3>", unsafe_allow_html=True)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload the resume.")

elif submit4:
    if uploaded_file:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt4)
            visualizations = False  # You can disable visualizations if not needed
            st.markdown("<h3 style='color: #4CAF50;'>Experience Level Match</h3>", unsafe_allow_html=True)
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload the resume.")

# Footer styling
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #808080;'>Powered by Gemini AI | Designed for ATS Matching</p>", unsafe_allow_html=True)