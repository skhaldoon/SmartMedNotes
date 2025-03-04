import os

class Config:
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')  # Path to your dataset folder
    PROCESSED_DIR = os.path.join(os.path.dirname(__file__), 'processed_data')  # Path to store processed files
    FAISS_INDEX_PATH = os.path.join(PROCESSED_DIR, "combined_faiss_index.faiss")  # Path to save FAISS index
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    SUMMARIZATION_MODEL = "t5-small"
    LLAMA_MODEL = "meta-llama/Llama-3.1-8B"

    # Ensure the processed data directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)