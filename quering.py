import json
import torch
from sentence_transformers import SentenceTransformer, util

# Default model and device setup
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_embeddings(embedding_path):
    """
    Load embeddings from a JSON file.
    """
    with open(embedding_path, 'r') as f:
        data = json.load(f)
    return data

def query_content(query, embeddings, model_name=MODEL_NAME, top_k=3, device=DEVICE):
    """
    Query the most relevant content using cosine similarity.
    """
    model = SentenceTransformer(model_name).to(device)  # Load model on the specified device
    query_embedding = model.encode(query, convert_to_tensor=True, device=device)
    
    results = []
    for item in embeddings:
        item_embedding = torch.tensor(item['embedding']).to(device)  # Convert to tensor
        score = util.cos_sim(query_embedding, item_embedding)[0].item()
        results.append((score, item['content']))
    
    # Sort results by similarity score
    results = sorted(results, key=lambda x: x[0], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    embedding_file = "/content/MayoClinic_embeddings.json"
    embeddings = load_embeddings(embedding_file)
    
    query = input("Enter your query: ")  # Allow dynamic input
    results = query_content(query, embeddings)

    print("\nTop Matching Results:")
    for score, content in results:
        print(f"\nScore: {score:.4f}\nContent: {content}\n")
