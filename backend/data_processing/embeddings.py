import os
from config import Config

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