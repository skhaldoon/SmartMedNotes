import os
from config import Config
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

def build_faiss_index():
    """
    Builds FAISS index from saved embeddings.
    """
    index = faiss.IndexFlatL2(384)  # Assuming MiniLM generates 384-d embeddings
    document_data = []
    
    embedding_files = [f for f in os.listdir(Config.PROCESSED_DIR) if f.endswith('_embeddings.npy')]
    
    for emb_file in embedding_files:
        emb_path = os.path.join(Config.PROCESSED_DIR, emb_file)
        doc_path = emb_path.replace('_embeddings.npy', '.json')
        
        embeddings = np.load(emb_path)
        with open(doc_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            document_data.extend([item['content'] for item in data])
        
        index.add(embeddings)
    
    return index, document_data

'''
def build_faiss_index():
    """Build a FAISS index from all processed JSON files."""
    json_files = [
        os.path.join(Config.PROCESSED_DIR, "MayoClinic_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "OrthopaedicTraumaForMedStudents_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "Osteoporosis-MayoClinic_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "info_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "orthopedics_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "speakingTree-Jayant_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "orthopedic_qa_embeddings.json"),
        os.path.join(Config.PROCESSED_DIR, "orthopedic_case_queries_embeddings.json")
    ]

    index, document_data = build_faiss_index(json_files, Config.FAISS_INDEX_PATH)
    return index, document_data
    '''