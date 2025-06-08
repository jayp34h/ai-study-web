# Study Notes Generator

A web application that generates study notes and quiz questions from textbook content or uploaded documents using AI.

## Features

- Text input via direct paste or document upload (PDF/DOCX)
- Generates organized bullet-point study notes
- Creates quiz questions (Multiple Choice, True/False, Short Answer)
- Clean and intuitive user interface
- Download generated content as text file

## Prerequisites

- Python 3.8 or higher
- Groq API key

## Installation

1. Clone the repository or download the files

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Running the Application

1. Navigate to the project directory
2. Run the Streamlit app:
```bash
streamlit run app.py
```
3. Open your web browser and go to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Choose your input method:
   - Upload a PDF or DOCX file
   - Paste text directly into the text area

2. Click the "Generate Notes & Questions" button

3. View the generated study materials:
   - Bullet-point study notes
   - Quiz questions (MCQ, True/False, Short Answer)

4. Download the generated content as a text file

## Project Structure

```
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── app.py             # Main Streamlit application
└── .env               # Environment variables (create this file)
```

## Dependencies

- streamlit: Web application framework
- langchain: LLM framework
- groq: Groq Cloud API client
- python-docx: DOCX file processing
- PyMuPDF: PDF file processing
- pdfplumber: PDF text extraction
- python-dotenv: Environment variable management

## Notes

- Make sure to keep your Groq API key secure and never commit it to version control
- Large documents may take longer to process
- The quality of generated notes and questions depends on the input text quality