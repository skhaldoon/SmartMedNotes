import json
import torch
from sentence_transformers import SentenceTransformer, util

def load_embeddings(embedding_path):
    """
    Load embeddings from a JSON file.
    """
    with open(embedding_path, 'r') as f:
        data = json.load(f)
    return data

def query_content(query, embeddings, model_name="sentence-transformers/all-MiniLM-L6-v2", top_k=3, device='cpu'):
    """
    Query the most relevant content using cosine similarity.
    """
    model = SentenceTransformer(model_name)
    model = model.to(device)  # Move the model to the specified device
    query_embedding = model.encode(query, convert_to_tensor=True, device=device)
    
    results = []
    for item in embeddings:
        # Convert item embedding (which is a list) to a tensor
        item_embedding = torch.tensor(item['embedding']).to(device)
        score = util.cos_sim(query_embedding, item_embedding)[0].item()
        results.append((score, item['content']))
    
    results = sorted(results, key=lambda x: x[0], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    embedding_file = '/content/MayoClinic_embeddings.json'
    embeddings = load_embeddings(embedding_file)
    query = "what is stress fracture"
    
    # You can specify the device here, for example, 'cpu' or 'cuda'
    device = 'cuda'  # or 'cuda' if you want to use GPU
    results = query_content(query, embeddings, device=device)
    
    for score, content in results:
        print(f"Score: {score:.4f}\nContent: {content}\n")
