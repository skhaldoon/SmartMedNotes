import re
import json
import os
import pandas as pd

def preprocess_text(file_path):
    """
    Comprehensive preprocessing pipeline for text files.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^A-Za-z0-9.,\s]', '', text)

    # Remove standalone page numbers, footnotes, and references
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'\d{1,4}[^A-Za-z0-9\s]', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\b\d{4}[;:](.*?)\b(?:Medline|CrossRef|PubMed)\b.*', '', text)
    text = re.sub(r'\b\w{2,}\d{1,2}\b.*', '', text)

    # Fix broken words and lines
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def convert_text_to_json(cleaned_text, input_path):
    """
    Converts preprocessed text into a JSON file.
    """
    if cleaned_text is None:
        print("Skipping JSON conversion due to preprocessing failure.")
        return

    paragraphs = cleaned_text.split('. ')
    json_data = [{"id": i + 1, "content": para.strip()} for i, para in enumerate(paragraphs) if para.strip()]

    output_path = os.path.join('/kaggle/working/', os.path.basename(input_path).replace('.txt', '.json'))

    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"JSON file saved at: {output_path}")
    except Exception as e:
        print(f"Error saving JSON file {output_path}: {e}")

def preprocess_csv(file_path):
    """
    Preprocess CSV files containing 'Question' and 'Answer' columns.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return None

    if 'Question' not in df.columns or 'Answer' not in df.columns:
        print(f"Invalid CSV format in {file_path}. Expected columns: 'Question', 'Answer'")
        return None

    df['Question'] = df['Question'].astype(str).apply(lambda x: preprocess_text_content(x))
    df['Answer'] = df['Answer'].astype(str).apply(lambda x: preprocess_text_content(x))

    json_data = df.to_dict(orient='records')
    return json_data

def preprocess_text_content(text):
    """Applies preprocessing to individual text content."""
    text = re.sub(r'[^A-Za-z0-9.,\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def convert_csv_to_json(file_path):
    """
    Converts a preprocessed CSV file into JSON format.
    """
    json_data = preprocess_csv(file_path)
    if json_data is None:
        return

    output_path = os.path.join('/kaggle/working/', os.path.basename(file_path).replace('.csv', '.json'))

    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"CSV converted to JSON and saved at: {output_path}")
    except Exception as e:
        print(f"Error saving JSON file {output_path}: {e}")

if __name__ == "__main__":
    text_files = [
        '/kaggle/input/orthopedics/MayoClinic.txt',
        '/kaggle/input/orthopedics/OrthopaedicTraumaForMedStudents.txt',
        '/kaggle/input/orthopedics/Osteoporosis-MayoClinic.txt',
        '/kaggle/input/orthopedics/info.txt',
        '/kaggle/input/orthopedics/orthopedics.txt',
        '/kaggle/input/orthopedics/speakingTree-Jayant.txt'
    ]
    csv_files = [
        '/kaggle/input/orthopedics/orthopedic_qa.csv',
        '/kaggle/input/orthopedics/orthopedic_case_queries.csv'
    ]

    for file_path in text_files:
        processed_text = preprocess_text(file_path)
        convert_text_to_json(processed_text, file_path)

    for file_path in csv_files:
        convert_csv_to_json(file_path)
