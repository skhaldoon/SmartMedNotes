import os

class Config:
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    PROCESSED_DIR = os.path.join(os.path.dirname(__file__), 'processed_data')
    FAISS_INDEX_PATH = os.path.join(PROCESSED_DIR, "combined_faiss_index.faiss")
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    SUMMARIZATION_MODEL = "t5-small"
    LLM_MODEL = "microsoft/phi-3-mini-4k-instruct"  # Changed to Phi-3
    FINE_TUNED_MODEL = "./fine_tuned_phi3"  # Path to save fine-tuned model

    os.makedirs(PROCESSED_DIR, exist_ok=True)