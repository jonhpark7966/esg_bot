import os
import pandas as pd
from pathlib import Path

def get_available_years():
    """Get available years from the data directory."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'reports')
    years = []
    if os.path.exists(data_dir):
        years = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    return sorted(years, reverse=True)

def get_available_companies(year):
    """Get available companies for a specific year."""
    if not year:
        return []
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'reports', str(year))
    companies = []
    if os.path.exists(data_dir):
        companies = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    return sorted(companies)

def get_explanations(year, company):
    """Get explanation markdown files for a specific company and year."""
    if not year or not company:
        return []
    
    explanations_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'data',
        'reports',
        str(year),
        company,
        'explanations'
    )

    questions_csv = pd.read_csv(os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'data','questions.csv'))
    
    questions = [] 
    explanations = []
    if os.path.exists(explanations_dir):
        for file in sorted(os.listdir(explanations_dir)):
            if file.endswith('.md'):
                file_path = os.path.join(explanations_dir, file)
                question_number = int(file.split('.')[0])
                content = questions_csv.loc[question_number, "question"]
                questions.append(content)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                explanations.append(content)
    return questions, explanations

def get_source_pdf(year, company):
    """Get the source PDF file path for a specific company and year."""
    if not year or not company:
        return None
    
    reports_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'data',
        'reports'
    )
    
    # Search for PDF files in the directory
    for file in os.listdir(reports_dir):
        if file.endswith('.pdf') and company.lower() in file.lower():
            return os.path.join(reports_dir, file)
    
    return None 

def load_data(year: str, company: str) -> pd.DataFrame:
    """
    Load the graded.csv file for the specified year and company.
    
    Args:
        year (str): The year to load data from
        company (str): The company name to load data for
        
    Returns:
        pd.DataFrame: The loaded data, or None if file doesn't exist
    """
    file_path = Path(f"data/reports/{year}/{company}/graded.csv")
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return None 