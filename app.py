import streamlit as st
import docx
import pdfplumber
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq LLM with llama-3.3-70b-versatile model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
    return text

def extract_text_from_docx(file):
    text = ""
    try:
        doc = docx.Document(file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {str(e)}")
    return text

def generate_notes_and_questions(text):
    # Template for generating study notes
    notes_template = """
    Based on the following text, create concise and organized bullet point study notes:
    
    {text}
    
    Format the notes in a clear, hierarchical structure with main points and sub-points.
    """
    
    # Template for generating quiz questions
    questions_template = """
    Based on the following text, generate a mix of quiz questions including:
    - 3 Multiple Choice Questions (MCQ)
    - 2 True/False Questions
    - 2 Short Answer Questions
    
    Text: {text}
    
    Format each question type separately and clearly.
    """
    
    # Create LangChain chains
    notes_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=notes_template, input_variables=["text"])
    )
    
    questions_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=questions_template, input_variables=["text"])
    )
    
    # Generate content
    notes = notes_chain.run(text=text)
    questions = questions_chain.run(text=text)
    
    return notes, questions

# Streamlit UI
st.set_page_config(page_title="Study Notes Generator", layout="wide")

st.title("📚 Study Notes Generator")
st.write("Upload a document or paste text to generate study notes and quiz questions!")

# Input method selection
input_method = st.radio("Choose input method:", ["Upload Document", "Paste Text"])

text_content = ""

if input_method == "Upload Document":
    uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx"])
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        with st.spinner("Extracting text from document..."):
            if file_type == "pdf":
                text_content = extract_text_from_pdf(uploaded_file)
            elif file_type == "docx":
                text_content = extract_text_from_docx(uploaded_file)
            
            if text_content:
                st.success("Text extracted successfully!")
            else:
                st.error("Failed to extract text from the document.")

else:  # Paste Text
    text_content = st.text_area("Paste your text here:", height=200)

if st.button("Generate Notes & Questions") and text_content:
    with st.spinner("Generating study materials..."):
        try:
            notes, questions = generate_notes_and_questions(text_content)
            
            # Display results in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Study Notes")
                st.markdown(notes)
                
            with col2:
                st.subheader("❓ Quiz Questions")
                st.markdown(questions)
                
            # Download options
            combined_content = f"STUDY NOTES\n\n{notes}\n\nQUIZ QUESTIONS\n\n{questions}"
            st.download_button(
                label="Download Notes & Questions",
                data=combined_content,
                file_name="study_materials.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Instructions in sidebar
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. Choose your input method:
        - Upload a PDF or DOCX file
        - Paste text directly
    2. Click 'Generate Notes & Questions'
    3. View your generated study materials
    4. Download the results as a text file
    """)
    
    st.header("About")
    st.markdown("""
    This app uses AI to help you create study materials from your text content.
    It generates:
    - Organized bullet-point notes
    - Multiple choice questions
    - True/False questions
    - Short answer questions
    """)