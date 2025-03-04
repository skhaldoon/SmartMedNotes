import os
from config import Config

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