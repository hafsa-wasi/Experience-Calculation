import PyPDF2
from datetime import datetime
import re

def extract_file(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() #5+5 1+1+1
    return text

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_experience_section(text):
    match = re.search(r'Experience\s*(.*?)\b(?:Education|Skills|Projects|Publications|Additional Experience|Technologies)\b', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def extract_all_dates(text):
    date_regex = re.compile(r'(\b\w{3,9}\s\d{4}\b)\s*[\–\-—–]+\s*(\b\w{3,9}\s\d{4}\b|\bPresent\b)', re.IGNORECASE)
    matches = date_regex.findall(text)
    return matches

def parse_date(date_str):
    for fmt in ('%b %Y', '%B %Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date {date_str} is not in a recognized format.")

def calculate_total_experience(date_ranges):
    total_months = 0

    for start_date, end_date in date_ranges:
        # Convert to datetime objects
        start_date = parse_date(start_date)
        end_date = datetime.now() if end_date.lower() == 'present' else parse_date(end_date)
        
        # Calculate the duration in months
        months_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
        total_months += months_diff

    # Convert total months to years and months
    years, months = divmod(total_months, 12)
    return years, months

def main(pdf_file):
    # Extract the resume text from PDF
    text = extract_file(pdf_file)
    
    # Normalize the resume text
    normalized_text = normalize_text(text)
    
    # Extract the Experience section
    experience_section = extract_experience_section(normalized_text)
    
    # Extract all date ranges from the Experience section
    date_ranges = extract_all_dates(experience_section)
    
    # Calculate total experience
    years, months = calculate_total_experience(date_ranges)
    
    # Output the results
    print(f"Total experience: {years} years and {months} months")


pdf_file = "Document.pdf"
main(pdf_file)
