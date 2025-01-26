import json
from sentence_transformers import SentenceTransformer

def generate_embeddings(data_path, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Generate embeddings for the dataset using SentenceTransformer.
    """
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    model = SentenceTransformer(model_name)
    embeddings = []
    for item in data:
        embedding = model.encode(item['content'], convert_to_tensor=True)
        embeddings.append({"content": item['content'], "embedding": embedding.tolist()})
    
    return embeddings

def save_embeddings(embeddings, output_path):
    """
    Save embeddings to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(embeddings, f, indent=4)

if __name__ == "__main__":
    json_file = '/content/MayoClinic.json'
    embeddings = generate_embeddings(json_file)
    save_embeddings(embeddings, json_file.replace('.json', '_embeddings.json'))
s