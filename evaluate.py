from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import json
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes and methods
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],  # Allow requests from your frontend
        "methods": ["POST", "OPTIONS"],  # Allow POST and OPTIONS methods
        "allow_headers": ["Content-Type"]  # Allow Content-Type header
    }
})

# Load Sentence-Transformer model
def load_embeddings(embedding_path):
    with open(embedding_path, 'r') as f:
        data = json.load(f)
    return data

def query_content(query, embeddings, model_name="sentence-transformers/all-MiniLM-L6-v2", top_k=3, device='cpu'):
    model = SentenceTransformer(model_name)
    model = model.to(device)
    query_embedding = model.encode(query, convert_to_tensor=True, device=device)
    
    results = []
    for item in embeddings:
        item_embedding = torch.tensor(item['embedding']).to(device)
        score = util.cos_sim(query_embedding, item_embedding)[0].item()
        results.append((score, item['content']))
    
    results = sorted(results, key=lambda x: x[0], reverse=True)
    return results[:top_k]

# Load embeddings once when the server starts
EMBEDDING_FILE = "/content/MayoClinic_embeddings.json"
embeddings = load_embeddings(EMBEDDING_FILE)

# Load GPT-2 model
MODEL_PATH = "./gpt2-finetuned"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH).to(device)

def generate_response(input_text, max_length=150):
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    outputs = model.generate(input_ids=input_ids, max_length=max_length, pad_token_id=tokenizer.eos_token_id,
                             temperature=0.5, top_k=50, top_p=0.95, no_repeat_ngram_size=2, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Define the route for Sentence-Transformer queries
# Define the route for Sentence-Transformer queries
@app.route("/all-MiniLM-L6-v2", methods=["POST", "OPTIONS"])
def query_miniLLM():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight request successful"}), 200

    data = request.json
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"error": "Query is empty"}), 400
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    results = query_content(user_query, embeddings, device=device)

    # Log the scores in the terminal, but only send the content to the frontend
    for score, content in results:
        print(f"Score: {score:.4f} | Content: {content[:50]}...")  # Print score with content (truncated for readability)

    formatted_results = [{"content": content} for _, content in results]  # Only send content to the frontend
    return jsonify({"response": formatted_results})

# Define the route for GPT-2 queries
@app.route("/gpt2", methods=["POST", "OPTIONS"])
def query_gpt2():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight request successful"}), 200

    data = request.json
    user_query = data.get("query", "")
    
    if not user_query:
        return jsonify({"error": "Query is empty"}), 400
    
    response_text = generate_response(user_query, max_length=150)
    return jsonify({"response": response_text})


if __name__ == "__main__":
    # Start ngrok and expose the Flask app
    public_url = ngrok.connect(5000).public_url  # Expose port 5000
    print(" * Public URL:", public_url)
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)