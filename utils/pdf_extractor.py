from pdfminer.high_level import extract_text
import json
import os

def extract_pdf_content(pdf_path):
    """Extracts text content from a PDF file."""
    return extract_text(pdf_path)

def save_to_json(course_name, text):
    """Saves extracted text content to a JSON file."""
    # Save results in 'C:/Users/admin/l7erf-bot/data'
    output_dir = "C:/Users/admin/l7erf-bot/data"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{course_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"content": text}, f, ensure_ascii=False, indent=4)

def process_all_pdfs(root_folder):
    """Recursively processes all PDFs in the root folder and subdirectories."""
    print(f"Scanning folder: {root_folder}")  # Debug print

    for dirpath, _, filenames in os.walk(root_folder):
        print(f"Checking directory: {dirpath}")  # Debug print

        for filename in filenames:
            if filename.endswith(".pdf"):
                try:
                    pdf_path = os.path.join(dirpath, filename)
                    course_name = os.path.splitext(filename)[0]

                    print(f"Processing: {course_name}")

                    text = extract_pdf_content(pdf_path)
                    save_to_json(course_name, text)

                    print(f"Saved: {course_name}.json")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

process_all_pdfs("C:/Users/admin/l7erf-bot/pdfs/S7")
