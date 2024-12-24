# ENSAM Chatbot

The **ENSAM Chatbot** is a multi-functional chatbot application designed for students of ENSAM Meknès. It integrates various features such as a PDF summarizer, general information about ENSAM, and a course-related chatbot, all within a sleek and interactive user interface powered by **Streamlit**.

## Features

1. **Summarization Bot**:
   - Upload PDFs and get automatic summarization in both **English** and **French**.
   - Key features include text extraction, OCR from images in PDFs, and structured note generation.

2. **General Info Bot**:
   - Provides detailed information about ENSAM Meknès, including academic tracks and extracurricular activities.
   - Uses **LangChain** with **Groq API** for real-time responses based on a knowledge base.

3. **Courses Bot**:
   - Responds to course-related queries using a **fine-tuned GPT model**.
   - Queries can be posed in French, with responses generated from the model's specialized training.

## Requirements

To run the application, ensure you have the following installed:

- Python 3.7+
- Streamlit
- Transformers
- LangChain
- PyMuPDF
- pdfplumber
- pytesseract
- pdf2image
- keybert
- Groq API (for General Info Bot)
- Other dependencies: `fitz`, `langdetect`, `Pillow`, `tempfile`

You can install the required libraries using `pip`:

```bash
pip install streamlit transformers langchain langchain_groq pytesseract pdfplumber pdf2image keybert langdetect pillow
