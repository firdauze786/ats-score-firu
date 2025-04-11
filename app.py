from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model version
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")  

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Job description input
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("✅ PDF Uploaded Successfully")

# User Inputs for Cover Letter
st.subheader("Cover Letter Details")
your_name = st.text_input("Your Name")
your_address = st.text_input("Your Address")
your_phone = st.text_input("Your Phone Number")
your_email = st.text_input("Your Email Address")
date = st.text_input("Date (e.g., March 19, 2025)")

hiring_manager_name = st.text_input("Hiring Manager's Name")
hiring_manager_title = st.text_input("Hiring Manager's Title")
company_name = st.text_input("Company Name")
company_address = st.text_input("Company Address")

salutation = st.text_input("Salutation (e.g., Dear Mr. Smith)")

# Buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")
submit4 = st.button("Generate Cover Letter")  # New button for cover letter

# Prompts
input_prompt1 = """    
You are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full Stack
Web Development, Big Data Engineering, DevOps, Data Analyst. Your task is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""  

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) Scanner with a deep understanding of any one job role (Data Science, 
Full Stack Web Development, Big Data Engineering, DevOps, Data Analyst) and ATS functionality.
Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. 
First, the output should come as percentage, then missing keywords, and finally, overall thoughts.
"""

# Cover Letter Prompt
input_prompt4 = f"""  
You are a professional career consultant specializing in writing *personalized cover letters*.  
Generate a *formal, engaging, and well-structured* cover letter using the following details:

Your Name: {your_name}  
Your Address: {your_address}  
Your Phone: {your_phone}  
Your Email: {your_email}  
Date: {date}  

Hiring Manager: {hiring_manager_name}  
Title: {hiring_manager_title}  
Company Name: {company_name}  
Company Address: {company_address}  

Salutation: {salutation}  

The cover letter should follow this structure:

1. *Introduction*: Express enthusiasm for the job.
2. *Skills & Experience*: Highlight key skills from the resume that match the job.
3. *Why This Role?*: Explain why the candidate is a great fit.
4. *Closing Statement*: End with a strong call to action.

Ensure the cover letter is *professional, concise, and compelling*.
"""

# Process Resume Evaluation
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("⚠️ Please upload the resume")

# Process Percentage Match
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("⚠️ Please upload the resume")

# Process Cover Letter Generation
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.subheader("Generated Cover Letter:")
        st.write(response)
    else:
        st.write("⚠️ Please upload the resume")

