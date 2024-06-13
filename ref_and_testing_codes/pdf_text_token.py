import os
from PyPDF2 import PdfReader
import tiktoken

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def count_tokens(text, model='text-embedding-ada-002'):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

def process_pdfs_in_directory(directory_path):
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
    results = {}
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory_path, pdf_file)
        extracted_text = extract_text_from_pdf(pdf_path)
        token_count = count_tokens(extracted_text)
        results[pdf_file] = token_count
    
    return results

directory_path = '../data/gri_standard/'
results = process_pdfs_in_directory(directory_path)

for pdf_file, token_count in results.items():
    print(f"{pdf_file}: {token_count} tokens")