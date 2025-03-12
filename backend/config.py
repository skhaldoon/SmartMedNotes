import os

class Config:
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    PROCESSED_DIR = os.path.join(os.path.dirname(__file__), 'processed_data')
    FAISS_INDEX_PATH = os.path.join(PROCESSED_DIR, "combined_faiss_index.faiss")
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    SUMMARIZATION_MODEL = "t5-small"

    # ✅ Update to load the fine-tuned model instead of base Phi-3
    FINE_TUNED_MODEL = os.path.join(os.path.dirname(__file__), "fine_tuned_phi3")
    PEFT_CONFIG = {
        "task_type": "CAUSAL_LM",
        "inference_mode": True,
        "layers_pattern": "model.layers",
        "target_modules": ["q_proj", "v_proj"]  # Match your adapter's training setup
    }