import streamlit as st
import pandas as pd
import os
import json
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv
import time
import google.generativeai as genai
#import gemini
import pdfplumber
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

summary=""
ajuste=""
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_accountZ.json"
#load_dotenv()
#openai.api_key = os.getenv('OPENAI_API_KEY')

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

def save_uploaded_file(uploaded_file, file_path):
    with open(file_path, 'wb') as resumenTxt:  # Use 'wb' for binary write mode
        resumenTxt.write(uploaded_file.getvalue())


prompt=[
 f"""
    You are an expert career coach who is going to do recommendations 
    according to the resume in {summary} and user goal contained in  {ajuste}:
   
    """
]

prompt2=[
        """por favor resume este texto
        """
]

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            text += page_text
    return text


## StreamliT
def main():
# Aplicacion Streamlit
    st.write("""# Coach carrer""")
    ajuste = st.text_input("What is your biggest carrer dream?")
    st.write(ajuste)
    
    if ajuste:  # Ejecutar solo si se proporciona un texto en el input
        
        response=get_gemini_response(ajuste,prompt)
        st.write(str(response))
        
   
   
 # SIDEBAR  DOCUMENTS UPLOAD
    with st.sidebar:
        uploaded_file = st.file_uploader("Please upload your resume")
        
    if uploaded_file is not None:
        try:
            pdf_text = extract_text_from_pdf(uploaded_file)
            #summarizer = gemini.Summarizer()
            summary = get_gemini_response(pdf_text,prompt2)
            st.write("**Summary:**")
            st.write(summary)
                        
        except Exception as e:
            st.error(f"Error processing the uploaded meeting file: {str(e)}")

    

if __name__ == "__main__":
    st.set_page_config(
        page_title="MilestoneMaster", page_icon="icono"
    )
    main()