import streamlit as st
import os
import time
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv
from prompts import ATS_PROMPT_TEMPLATE

# Load env
load_dotenv()

# Constants
API_KEY = os.getenv(key="GOOGLE_API_KEY")

# API Setup
genai.configure(api_key=API_KEY)


def get_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


def get_gemini_response(input_prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(contents=input_prompt)
    return response.text


def app():
    st.set_page_config(page_title="Smart ATS")
    st.header("ATS System Using Google's Gemini Pro")
    # Input
    job_description = st.text_area(label="Job Description here:")
    uploaded_file = st.file_uploader(
        label="Your Resume Here:",
        type='pdf',
        help="Please upload pdf resume."
    )

    # Submit button
    submit = st.button(label="Submit")
    if submit:
        if uploaded_file is not None:
            text = get_pdf_text(uploaded_file)
            response = get_gemini_response(ATS_PROMPT_TEMPLATE)
            st.subheader("Response:")
            st.write(response)


if __name__ == '__main__':
    app()
