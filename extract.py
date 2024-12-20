import os
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from config import *  


pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


def extract_text_from_pdf(file_path):
    try:
        text = ""
        document = fitz.open(file_path)
        for page in document:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

# Function to extract text from DOCX
def extract_text_from_docx(file_path):
    try:
        document = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return text
    except Exception as e:
        return f"Error extracting text from DOCX: {e}"

# Function to extract text from images
def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error extracting text from image: {e}"

# Function to process each file based on its type
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(file_path)
    else:
        return "Unsupported file format."

# Function to process all files in a folder
def extract_text_from_folder(folder_path):
    extracted_texts = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            print(f"Processing: {file_name}")
            extracted_texts[file_name] = extract_text(file_path)
    return extracted_texts

# Example usage
if __name__ == "__main__":
    folder_path = FOLDER_PATH  # Replace with your folder path
    extracted_texts = extract_text_from_folder(folder_path)

    # Save the extracted texts to a file for review
    output_file = OUTPUT_PATH + "/result.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for file_name, text in extracted_texts.items():
            f.write(f"--- {file_name} ---\n{text}\n\n")
    
    print(f"Text extraction completed. Results saved to {output_file}.")