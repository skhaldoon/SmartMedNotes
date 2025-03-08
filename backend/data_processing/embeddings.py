import os
from config import Config
import json
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def generate_embeddings(json_file):
    """
    Generate embeddings for a JSON file.
    """
    model = SentenceTransformer(Config.MODEL_NAME)
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        texts = [item['content'] for item in data]
        embeddings = model.encode(texts, convert_to_numpy=True).astype(np.float32)
        return embeddings
    except Exception as e:
        logging.error(f"Error generating embeddings for {json_file}: {e}")
        return None

def save_embeddings(embeddings, json_file):
    """
    Save embeddings as a NumPy file.
    """
    try:
        emb_path = json_file.replace('.json', '_embeddings.npy')
        np.save(emb_path, embeddings)
        logging.info(f"Saved embeddings: {emb_path}")
    except Exception as e:
        logging.error(f"Error saving embeddings: {e}")

def generate_all_embeddings():
    """Generate embeddings for all processed JSON files."""
    json_files = [
        os.path.join(Config.PROCESSED_DIR, "MayoClinic.json"),
        os.path.join(Config.PROCESSED_DIR, "OrthopaedicTraumaForMedStudents.json"),
        os.path.join(Config.PROCESSED_DIR, "Osteoporosis-MayoClinic.json"),
        os.path.join(Config.PROCESSED_DIR, "info.json"),
        os.path.join(Config.PROCESSED_DIR, "orthopedics.json"),
        os.path.join(Config.PROCESSED_DIR, "speakingTree-Jayant.json"),
        os.path.join(Config.PROCESSED_DIR, "orthopedic_qa.json"),
        os.path.join(Config.PROCESSED_DIR, "orthopedic_case_queries.json")
    ]

    for json_file in json_files:
        embeddings = generate_embeddings(json_file)
        if embeddings:
            save_embeddings(embeddings, json_file)