from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from models.retriever import retrieve_faiss_docs
from models.summarizer import summarize_context
from models.llama import generate_response
from data_processing.faiss_index import build_faiss_index
from data_processing.preprocess import preprocess_all_files
from data_processing.embeddings import generate_all_embeddings
from config import Config
import os

# Preprocess dataset and build FAISS index on startup
try:
    preprocess_all_files()
    generate_all_embeddings()
except Exception as e:
    logging.error(f"Failed to preprocess data or generate embeddings: {e}")
    exit(1)

try:
    faiss_index, document_data = build_faiss_index()
    if faiss_index is None or document_data is None:
        raise Exception("Failed to build FAISS index.")
except Exception as e:
    logging.error(f"Failed to build FAISS index: {e}")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Setup Flask app
app = Flask(__name__)
CORS(app)

@app.route("/rag", methods=["POST"])
def rag_pipeline():
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

    context = summarize_context(" ".join(retrieved_docs))
    response = generate_response(context, user_query)
    logging.info(f"Generated response: {response}")

    return jsonify({"query": user_query, "response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
