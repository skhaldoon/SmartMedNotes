import json
import torch
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
from glob import glob

def build_faiss_index(json_files, index_path):
    """
    Build a FAISS index from multiple JSON embedding files.
    :param json_files: List of JSON file paths containing embeddings.
    :param index_path: Path to save the FAISS index.
    """
    all_embeddings = []
    document_data = []

    # Load embeddings from all JSON files
    for file in json_files:
        print(f"Processing: {file}")
        with open(file, 'r') as f:
            data = json.load(f)

        for item in data:
            if 'embedding' in item and ('content' in item or 'Question' in item):
                all_embeddings.append(np.array(item['embedding'], dtype=np.float32))
                # Combine Question and Answer as content
                text = item.get('content', f"Q: {item.get('Question', '')} A: {item.get('Answer', '')}")
                document_data.append(text)
            else:
                print(f"⚠️ Skipping entry in {file}: Missing 'embedding' or valid text field")

    # Convert to FAISS format
    if all_embeddings:
        dimension = len(all_embeddings[0])  # Embedding size
        index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean) Index
        index.add(np.array(all_embeddings, dtype=np.float32))  # Add all embeddings

        # Save index and document data
        faiss.write_index(index, index_path)
        with open(index_path.replace('.faiss', '_docs.json'), 'w') as f:
            json.dump(document_data, f)

        print(f"✅ FAISS index saved at: {index_path}")
        return index, document_data
    else:
        print("❌ No valid embeddings found.")
        return None, None

# Example usage
json_files = [
    "/kaggle/working/MayoClinic_embeddings.json",
    "/kaggle/working/speakingTree-Jayant_embeddings.json",
    "/kaggle/working/orthopedics_embeddings.json",
    "/kaggle/working/info_embeddings.json",
    "/kaggle/working/orthopedic_qa_embeddings.json",
    "/kaggle/working/orthopedic_case_queries_embeddings.json"
]

faiss_index, document_data = build_faiss_index(json_files, "/kaggle/working/combined_faiss_index.faiss")
