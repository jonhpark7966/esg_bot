import fitz  # PyMuPDF
import os
import re

def extract_chunks(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    text = ""
    
    # Extract text from each page
    for page_num in range(len(document)):
        page = document[page_num]
        text += page.get_text()
    
    # Identify the chunks based on the contents page
    contents_pattern = re.compile(r'(\d+\.\s+[A-Za-z ]+\s+\d+)')
    contents_matches = contents_pattern.findall(text)
    
    # Create a list of chunks based on the matches
    chunks = []
    for match in contents_matches:
        # Extract the section title and starting page number
        section_title, starting_page = match.rsplit(' ', 1)
        starting_page = int(starting_page) - 1  # Page numbers in PDF are 0-based
        
        # Find the text for each chunk
        chunk_text = ""
        for page_num in range(starting_page, len(document)):
            page = document[page_num]
            chunk_text += page.get_text()
            if contents_pattern.search(page.get_text()):
                break
        
        chunks.append((section_title, chunk_text))
    
    return chunks

def save_chunks_as_files(chunks, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, (title, text) in enumerate(chunks):
        filename = f"chunk_{i+1}_{title.replace(' ', '_')}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)

def process_pdf_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            chunks = extract_chunks(pdf_path)
            output_dir = os.path.join(directory, filename[:-4] + "_chunks")
            save_chunks_as_files(chunks, output_dir)
            print(f"Processed {filename} and saved chunks to {output_dir}")

if __name__ == "__main__":
    pdf_directory = "../data/gri_standard/"
    process_pdf_files(pdf_directory)
