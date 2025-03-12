#PREPROCESSING AND CONVERSION TO JSON FOR BETTER STRUCTURE
import os
import json
import logging
import pandas as pd

# ✅ Define paths for Kaggle
DATA_DIR = "/kaggle/input/orthopedics"  # Update if needed
PROCESSED_DIR = "/kaggle/working/processed_data"

# ✅ Ensure processed_data directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ✅ Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Function to process TXT files
def preprocess_text(file_path):
    """Reads and cleans text files, then converts them to structured JSON format."""
    if not os.path.exists(file_path):
        logging.warning(f"❌ Skipping {file_path}: File not found.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()

        if not text:
            logging.warning(f"❌ Skipping {file_path}: File is empty.")
            return None

        return text.replace('\n', ' ').strip()

    except Exception as e:
        logging.error(f"❌ Error processing {file_path}: {e}")
        return None

# ✅ Function to process CSV files
def preprocess_csv(file_path):
    """Handles CSV files with flexible column names and converts them into structured JSON."""
    if not os.path.exists(file_path):
        logging.warning(f"❌ Skipping {file_path}: File not found.")
        return None

    try:
        df = pd.read_csv(file_path)
        
        # ✅ Ensure CSV is not empty
        if df.empty:
            logging.warning(f"❌ Skipping {file_path}: CSV file is empty.")
            return None

        # ✅ Case-insensitive column matching
        col_map = {
            'question': ['question', 'Question', 'query', 'Query'],
            'answer': ['answer', 'Answer', 'response', 'Response']
        }

        found_columns = {}
        for col_type, possible_names in col_map.items():
            for col_name in possible_names:
                if col_name in df.columns:
                    found_columns[col_type] = col_name
                    break  # Stop checking after first match

        # ✅ Verify we found both required columns
        if 'question' not in found_columns or 'answer' not in found_columns:
            logging.warning(f"❌ CSV structure error in {file_path}: Required columns missing.")
            return None

        # ✅ Convert CSV to structured JSON format
        json_data = [
            {
                "id": i + 1,
                "content": f"Q: {row[found_columns['question']]} | A: {row[found_columns['answer']]}"
            }
            for i, row in df.iterrows()
        ]

        return json_data

    except Exception as e:
        logging.error(f"❌ Error processing CSV {file_path}: {e}")
        return None

# ✅ Function to process all dataset files (TXT & CSV)
def preprocess_all_files():
    """Preprocess both TXT and CSV files in the dataset directory."""
    text_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    csv_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.csv')]

    # ✅ Process TXT files
    for file_path in text_files:
        output_path = os.path.join(PROCESSED_DIR, os.path.basename(file_path).replace('.txt', '.json'))
        if os.path.exists(output_path):
            logging.info(f"✅ {output_path} already exists. Skipping...")
            continue
        text = preprocess_text(file_path)
        if text:
            convert_text_to_json(text, output_path)

    # ✅ Process CSV files
    for file_path in csv_files:
        output_path = os.path.join(PROCESSED_DIR, os.path.basename(file_path).replace('.csv', '.json'))
        if os.path.exists(output_path):
            logging.info(f"✅ {output_path} already exists. Skipping...")
            continue
        data = preprocess_csv(file_path)
        if data:
            save_json(data, output_path)

# ✅ Function to convert TXT content into JSON format
def convert_text_to_json(cleaned_text, output_path):
    """Converts TXT files into structured JSON format with 'content' key."""
    paragraphs = cleaned_text.split('. ')  # ✅ Splitting into sentences
    json_data = [{"id": i + 1, "content": para.strip()} for i, para in enumerate(paragraphs) if para.strip()]

    save_json(json_data, output_path)

# ✅ Function to save any structured JSON format
def save_json(data, output_path):
    """Saves structured JSON format."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"✅ JSON file saved: {output_path}")
    except Exception as e:
        logging.error(f"❌ Error saving JSON file {output_path}: {e}")


