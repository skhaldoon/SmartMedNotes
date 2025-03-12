#EMBEDDINGS GENERATION 
import os
import json
import logging
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Define paths specific to Kaggle
PROCESSED_DIR = "/kaggle/working/processed_data"  # Processed data location (read/write allowed)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Embedding model

# ✅ Ensure processed_data directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ✅ Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_embeddings(json_file):
    """Generate and save embeddings for a JSON file."""
    if not os.path.exists(json_file):
        logging.warning(f"Skipping {json_file}: File not found.")
        return None

    emb_path = json_file.replace('.json', '_embeddings.npy').replace("/kaggle/input/", "/kaggle/working/")
    if os.path.exists(emb_path):
        logging.info(f"Skipping {json_file}: Embeddings already exist.")
        return None

    logging.info(f"Generating embeddings for {json_file}...")
    
    model = SentenceTransformer(MODEL_NAME)
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    texts = [item['content'] for item in data]
    embeddings = model.encode(texts, convert_to_numpy=True).astype(np.float32)

    np.save(emb_path, embeddings)
    logging.info(f"Saved embeddings: {emb_path}")
    return embeddings

def generate_all_embeddings():
    """Generate embeddings for all processed JSON files."""
    json_files = [os.path.join(PROCESSED_DIR, f) for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]

    for json_file in json_files:
        generate_embeddings(json_file)


