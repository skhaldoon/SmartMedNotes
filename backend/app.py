from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from models.retriever import retrieve_faiss_docs
from models.summarizer import summarize_context
from models.phi3 import generate_response  # Changed import
from data_processing.faiss_index import build_faiss_index
from data_processing.preprocess import preprocess_all_files
from data_processing.embeddings import generate_all_embeddings
from config import Config
import os
import nltk  # Added for punkt download

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)

# Preprocess dataset and build FAISS index on startup
try:
    if not os.path.exists(Config.PROCESSED_DIR) or not os.listdir(Config.PROCESSED_DIR):
        logging.info("Preprocessing data files...")
        preprocess_all_files()
        generate_all_embeddings()
except Exception as e:
    logging.error(f"Failed to preprocess data: {str(e)}")
    exit(1)

try:
    logging.info("Building FAISS index...")
    faiss_index, document_data = build_faiss_index()
    if faiss_index is None or document_data is None:
        raise RuntimeError("FAISS index initialization failed")
    logging.info(f"FAISS index built with {len(document_data)} documents")
except Exception as e:
    logging.error(f"FAISS index error: {str(e)}")
    exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Setup Flask app
app = Flask(__name__)
CORS(app, resources={r"/rag": {"origins": "*"}})

@app.route("/rag", methods=["POST"])
def rag_pipeline():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Invalid request format"}), 400
            
        user_query = data['query'].strip()
        if not user_query:
            return jsonify({"error": "Empty query"}), 400

        logging.info(f"Processing query: {user_query[:50]}...")
        
        # Retrieve documents
        retrieved_docs = retrieve_faiss_docs(user_query, faiss_index, document_data)
        if not retrieved_docs:
            return jsonify({"error": "No relevant documents found"}), 404

        # Process context
        context = " ".join(retrieved_docs)
        summarized_context = summarize_context(context)
        
        # Generate response
        response = generate_response(summarized_context, user_query)
        
        # Validate response
        if not response.endswith(('.', '!', '?')):
            response += '.'
            
        return jsonify({
            "query": user_query,
            "context": summarized_context[:200] + "...",  # For debugging
            "response": response
        })

    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=False)