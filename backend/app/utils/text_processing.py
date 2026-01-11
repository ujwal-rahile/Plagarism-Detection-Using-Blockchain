
import hashlib
from docx import Document
from PyPDF2 import PdfReader

def generate_hash(text):
    """Calculate the SHA256 hash of a given text."""
    if not text:
        return None
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text.encode('utf-8'))
    return sha256_hash.hexdigest()

def extract_text_chunks(filename):
    """
    Extracts text from PDF, DOCX, or TXT files and splits them into chunks (sentences).
    Returns a tuple: (list of SHA256 hashes, list of original text segments).
    """
    hashes = []
    text_segments = []

    try:
        if filename.endswith(".pdf"):
            reader = PdfReader(filename)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_segments.extend(text.strip().split("."))
        
        elif filename.endswith((".docx", ".doc")):
            doc = Document(filename)
            for paragraph in doc.paragraphs:
                text_segments.append(paragraph.text.strip())
        
        else:
            # Default to text file
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                # Initial cleanup matches original logic
                content = content.strip().replace('\n', '') 
                text_segments = content.split('.')

        # Process segments to keep aligned lists
        final_hashes = []
        final_segments = []
        
        for segment in text_segments:
            segment = segment.strip()
            if segment:
                hashed = generate_hash(segment)
                if hashed:
                    final_hashes.append(hashed)
                    final_segments.append(segment)
        
        return final_hashes, final_segments

    except Exception as e:
        print(f"Error processing file {filename}: {e}")
        return []
