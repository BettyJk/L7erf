from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer, T5Tokenizer, T5ForConditionalGeneration
import streamlit as st
import fitz  
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from langdetect import detect
from keybert import KeyBERT
from concurrent.futures import ThreadPoolExecutor
import re
import os
import logging
import tempfile
from typing import Tuple, List, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def load_summarization_models():
    try:
        summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        summarizer_fr = pipeline("summarization", model="moussaKam/mbarthez-dialogue-summarization", device=-1)
        return summarizer_en, summarizer_fr
    except Exception as e:
        logger.error(f"Error loading summarization models: {e}")
        return None, None

summarizer_en, summarizer_fr = load_summarization_models()
kw_model = KeyBERT()
flan_tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
flan_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

def is_valid_pdf(file_path: str) -> bool:
    try:
        with fitz.open(file_path) as pdf:
            return pdf.page_count > 0
    except Exception as e:
        logger.error(f"PDF validation error: {e}")
        return False

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
    return text

def extract_tables_from_pdf(pdf_path: str) -> List[pd.DataFrame]:
    tables_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    tables_data.append(df)
    except Exception as e:
        logger.error(f"Table extraction error: {e}")
    return tables_data

def extract_images_and_ocr(pdf_path: str, max_pages: int = 5) -> str:
    ocr_text = ""
    try:
        images = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=max_pages)
        for img in images:
            ocr_text += pytesseract.image_to_string(img, lang='eng+fra')
    except Exception as e:
        logger.error(f"OCR extraction error: {e}")
    return ocr_text

def get_summarizer(text: str) -> Tuple:
    language = detect(text)
    if language == "fr":
        return summarizer_fr, "French"
    elif language == "en":
        return summarizer_en, "English"
    else:
        return summarizer_en, "English"

def summarize_text(text: str, length: str = 'medium') -> str:
    summarizer, language = get_summarizer(text)
    if summarizer is None:
        return "Error: Summarizer model not available."

    # Configure summary length
    length_map = {'short': (50, 100), 'medium': (100, 150), 'long': (150, 200)}
    min_len, max_len = length_map.get(length, (100, 150))

    # Split and summarize in chunks if text is long
    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    
    return " ".join(summaries)

def extract_keywords(text: str) -> List[str]:
    language = detect(text)
    stop_words = 'french' if language == 'fr' else 'english'
    return [kw[0] for kw in kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words=stop_words, top_n=10)]

def generate_structured_notes(summary: str, language: str) -> str:
    prompt = (
        f"Organize the following summary into structured notes with sections and bullet points in {language}:\n\n"
        f"{summary}\n\nStructure:\n- **Introduction**\n- **Key Points**\n- **Conclusion**"
    )
    inputs = flan_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = flan_model.generate(inputs['input_ids'], max_length=512, num_return_sequences=1, temperature=0.7)
    return flan_tokenizer.decode(outputs[0], skip_special_tokens=True)

def extract_content_from_pdf(pdf_file) -> Tuple[str, List[pd.DataFrame], str]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file.read())
        temp_path = temp_file.name

    if not is_valid_pdf(temp_path):
        return "", [], ""

    with ThreadPoolExecutor() as executor:
        future_text = executor.submit(extract_text_from_pdf, temp_path)
        future_tables = executor.submit(extract_tables_from_pdf, temp_path)
        future_ocr = executor.submit(extract_images_and_ocr, temp_path, max_pages=5)

        extracted_text = future_text.result()
        extracted_tables = future_tables.result()
        extracted_ocr = future_ocr.result()

    combined_text = extracted_text or extracted_ocr
    os.remove(temp_path)
    return combined_text, extracted_tables, extracted_ocr

# Streamlit App
st.title("Advanced Multilingual PDF Summarizer and Note Organizer")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    st.info("Processing PDF, please wait...")
    text, tables, ocr_text = extract_content_from_pdf(uploaded_file)

    if not text:
        st.error("Failed to extract content from the PDF.")
    else:
        language = "French" if detect(text) == 'fr' else "English"
        st.success(f"Content extracted successfully! Detected Language: {language}")

        summary_length = st.radio("Select summarization depth:", ["short", "medium", "long"])
        summary = summarize_text(text, length=summary_length)
        keywords = extract_keywords(text)

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Keywords")
        st.write(", ".join(keywords))

        with st.spinner("Generating structured notes..."):
            notes = generate_structured_notes(summary, language)
        st.subheader("Organized Notes")
        st.write(notes)

        if tables:
            st.subheader("Extracted Tables")
            for i, table in enumerate(tables):
                st.write(f"Table {i+1}")
                st.dataframe(table)

        if ocr_text:
            st.subheader("OCR Text")
            st.text_area("Extracted Text from Images", ocr_text)
