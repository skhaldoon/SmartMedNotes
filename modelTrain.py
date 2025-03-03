import nltk
import json
import torch
import faiss
import logging
from pyngrok import ngrok
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

from huggingface_hub import login
hf_token = os.getenv("HUGGINGFACE_TOKEN")

if hf_token:
    login(hf_token)

# Download necessary NLTK components
nltk.download("punkt")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Setup Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

# Load Models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
retriever = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2").to(device).eval()

# Load Summarization Model (T5-small for efficiency)
sum_tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
sum_model = T5ForConditionalGeneration.from_pretrained("t5-small").to(device).eval()

# Load LLaMA-3 for response generation
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.float16,
    device_map="auto"
)

def load_faiss_index(index_path):
    """ Load FAISS index and corresponding document metadata. """
    try:
        index = faiss.read_index(index_path)
        with open(index_path.replace('.faiss', '_docs.json'), 'r') as f:
            document_data = json.load(f)
        return index, document_data
    except Exception as e:
        logging.error(f"Error loading FAISS index: {e}")
        return None, None

# Load the FAISS index
faiss_index, document_data = load_faiss_index("/kaggle/working/combined_faiss_index.faiss")

def retrieve_faiss_docs(query, index, document_data, top_k=3):
    """ Retrieve relevant documents using FAISS similarity search. """
    query_emb = retriever.encode(query, convert_to_numpy=True).astype(np.float32).reshape(1, -1)
    distances, indices = index.search(query_emb, top_k)
    
    results = []
    for i in indices[0]:
        if i < len(document_data):
            doc_text = document_data[i]
            results.append(doc_text)

    return results

def summarize_context(context):
    """ Summarize retrieved documents to make context concise. """
    if not context:
        return ""
    
    input_text = "summarize: " + context
    input_ids = sum_tokenizer.encode(input_text, return_tensors="pt").to(device)
    summary_ids = sum_model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    
    return sum_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def generate_response(context, query, max_new_tokens=200):
    """
    Generate a response using LLaMA-3 with improved sentence completion.
    """
    input_text = f"Context: {context}\nQuery: {query}\nAnswer:"
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)

    output = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        no_repeat_ngram_size=3
    )

    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract answer after "Answer:"
    answer_start = response_text.find("Answer:")
    raw_answer = response_text[answer_start + len("Answer:"):].strip() if answer_start != -1 else response_text.strip()

    # Ensure the answer ends at a proper sentence boundary
    sentences = nltk.sent_tokenize(raw_answer)
    final_answer = " ".join(sentences[: min(len(sentences), 5)])

    return final_answer
    
@app.route("/rag", methods=["POST"])
def rag_pipeline():
    """ Handles incoming user queries and generates AI-powered responses. """
    data = request.json
    user_query = data.get("query", "").strip()
    
    if not user_query:
        logging.warning("Empty query received.")
        return jsonify({"error": "Query is empty"}), 400

    logging.info(f"Received query: {user_query}")
    
    retrieved_docs = retrieve_faiss_docs(user_query, faiss_index, document_data)
    logging.info(f"Retrieved documents: {retrieved_docs}")

    if not retrieved_docs:
        return jsonify({"error": "No relevant documents found."}), 404

    context = summarize_context(" ".join(retrieved_docs))  # Summarize retrieved docs
    response = generate_response(context, user_query)
    logging.info(f"Generated response: {response}")

    return jsonify({"query": user_query, "response": response})
    
if __name__ == "__main__":
    try:
        public_url = ngrok.connect(5000).public_url
        print(" * Public URL:", public_url)
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        logging.error(f"Server startup failed: {e}")
