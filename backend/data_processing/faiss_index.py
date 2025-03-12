# data_processing/faiss_index.py
import os
import json
import faiss

def load_faiss_index():
    """Load prebuilt FAISS index and document data for Hugging Face deployment"""
    # Paths relative to project root
    FAISS_INDEX_PATH = "processed_data/combined_faiss_index.faiss"
    DOC_DATA_PATH = "processed_data/document_data.json"
    
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}")
    if not os.path.exists(DOC_DATA_PATH):
        raise FileNotFoundError(f"Document data not found at {DOC_DATA_PATH}")

    # Load the prebuilt index
    index = faiss.read_index(FAISS_INDEX_PATH)
    
    # Load document texts
    with open(DOC_DATA_PATH, "r", encoding="utf-8") as f:
        document_data = json.load(f)
    
    # Validate index-document alignment
    if len(document_data) != index.ntotal:
        raise RuntimeError(
            f"Data mismatch: {len(document_data)} docs vs {index.ntotal} embeddings"
        )
    
    print(f"✅ Loaded FAISS index with {index.ntotal} entries and {len(document_data)} documents")
    return index, document_data