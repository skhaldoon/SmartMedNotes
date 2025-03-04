import os
from config import Config

def preprocess_all_files():
    """Preprocess all text and CSV files in the data folder."""
    text_files = [
        os.path.join(Config.DATA_DIR, "MayoClinic.txt"),
        os.path.join(Config.DATA_DIR, "OrthopaedicTraumaForMedStudents.txt"),
        os.path.join(Config.DATA_DIR, "Osteoporosis-MayoClinic.txt"),
        os.path.join(Config.DATA_DIR, "info.txt"),
        os.path.join(Config.DATA_DIR, "orthopedics.txt"),
        os.path.join(Config.DATA_DIR, "speakingTree-Jayant.txt")
    ]
    csv_files = [
        os.path.join(Config.DATA_DIR, "orthopedic_qa.csv"),
        os.path.join(Config.DATA_DIR, "orthopedic_case_queries.csv")
    ]

    # Preprocess text files
    for file_path in text_files:
        processed_text = preprocess_text(file_path)
        if processed_text:
            convert_text_to_json(processed_text, file_path)

    # Preprocess CSV files
    for file_path in csv_files:
        convert_csv_to_json(file_path)

def convert_text_to_json(cleaned_text, input_path):
    """
    Converts preprocessed text into a JSON file and saves it in the processed_data folder.
    """
    if cleaned_text is None:
        print("Skipping JSON conversion due to preprocessing failure.")
        return

    paragraphs = cleaned_text.split('. ')
    json_data = [{"id": i + 1, "content": para.strip()} for i, para in enumerate(paragraphs) if para.strip()]

    output_path = os.path.join(Config.PROCESSED_DIR, os.path.basename(input_path).replace('.txt', '.json'))

    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"JSON file saved at: {output_path}")
    except Exception as e:
        print(f"Error saving JSON file {output_path}: {e}")

def convert_csv_to_json(file_path):
    """
    Converts a preprocessed CSV file into JSON format and saves it in the processed_data folder.
    """
    json_data = preprocess_csv(file_path)
    if json_data is None:
        return

    output_path = os.path.join(Config.PROCESSED_DIR, os.path.basename(file_path).replace('.csv', '.json'))

    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        print(f"CSV converted to JSON and saved at: {output_path}")
    except Exception as e:
        print(f"Error saving JSON file {output_path}: {e}")