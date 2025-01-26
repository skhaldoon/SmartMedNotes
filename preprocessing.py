import re
import json
import os

def preprocess_text(file_path):
    """
    Comprehensive preprocessing pipeline:
    - Removes special characters (except basic punctuation for sentence structure)
    - Handles page numbers, footnotes, and references
    - Fixes broken lines/words
    - Removes extra spaces
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

    # Step 1: Remove special characters (but keep basic punctuation)
    text = re.sub(r'[^A-Za-z0-9.,\s]', '', text)  # Keeps '.', ',' for sentence structure

    # Step 2: Remove standalone page numbers and footnotes
    text = re.sub(r'\b\d+\b', '', text)  # Removes standalone numbers (e.g., page numbers)
    text = re.sub(r'\d{1,4}[^A-Za-z0-9\s]', '', text)  # Removes numbers followed by special characters

    # Step 3: Remove references and citations
    text = re.sub(r'\[.*?\]', '', text)  # Removes inline references like [1], [2]
    text = re.sub(r'\b\d{4}[;:](.*?)\b(?:Medline|CrossRef|PubMed)\b.*', '', text)  # Removes Medline citations
    text = re.sub(r'\b\w{2,}\d{1,2}\b.*', '', text)  # Removes alphanumeric references (e.g., TSRH23)

    # Step 4: Fix broken lines and words
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Fix broken words split across lines
    text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space

    # Step 5: Remove leading/trailing spaces
    text = text.strip()

    return text


def convert_to_json(cleaned_text, output_path):
    """
    Converts preprocessed text into a JSON file, splitting the text into sections or paragraphs.
    Each paragraph is stored as an individual JSON entry.
    """
    if cleaned_text is None:
        print(f"Skipping JSON conversion as text preprocessing failed.")
        return
    
    # Split the text into paragraphs (use '. ' for sentence splitting)
    paragraphs = cleaned_text.split('. ')  # Split by sentences for structured JSON
    
    # Structure each paragraph as a JSON object
    json_data = [{"id": i + 1, "content": para.strip()} for i, para in enumerate(paragraphs) if para.strip()]
    
    # Save to JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"JSON file saved at: {output_path}")
    except Exception as e:
        print(f"Error saving JSON file {output_path}: {e}")


if __name__ == "__main__":
    # Example file paths
    file_paths = [
        '/content/MayoClinic.txt',
        '/content/Osteoporosis-MayoClinic.txt',
        '/content/speakingTree-Jayant.txt',
        '/content/MayoClinic.txt'
    ]
    
    for file_path in file_paths:
        # Preprocess the file
        processed = preprocess_text(file_path)
        
        # Create output JSON path
        json_path = file_path.replace('.txt', '.json')
        
        # Convert preprocessed text to JSON
        convert_to_json(processed, json_path)
