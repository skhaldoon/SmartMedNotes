from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging
import os
from models.retriever import retrieve_faiss_docs
from models.summarizer import summarize_context
from models.phi3 import generate_response
from data_processing.faiss_index import load_faiss_index
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load FAISS index
if not os.path.exists("processed_data/combined_faiss_index.faiss"):
    logging.error("FAISS index not found! Please generate it before deployment.")
    raise FileNotFoundError("FAISS index is missing")
else:
    logging.info("Loading existing FAISS index...")
    faiss_index, document_data = load_faiss_index()

# Ensure fine-tuned model is loaded
if not os.path.exists("fine_tuned_phi3"):
    logging.error("Fine-tuned model not found!")
    raise FileNotFoundError("Fine-tuned model is missing")

# Initialize FastAPI
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    
@app.get("/")
async def home():
    return {"message": "FastAPI backend is running on Hugging Face Spaces!"}
    
@app.post("/rag")
async def rag_pipeline(request: QueryRequest):
    user_query = request.query.strip()
    
    if not user_query:
        logging.warning("Empty query received.")
        raise HTTPException(status_code=400, detail="Query is empty")

    logging.info(f"Received query: {user_query}")
    
    retrieved_docs = retrieve_faiss_docs(user_query, faiss_index, document_data)
    logging.info(f"Retrieved {len(retrieved_docs)} documents.")

    if not retrieved_docs:
        logging.warning("No relevant documents found.")
        return {"query": user_query, "response": "Sorry, no relevant information found."}

    context = summarize_context(" ".join(retrieved_docs))
    response = generate_response(context, user_query)
    logging.info("Generated response.")

    return {"query": user_query, "response": response}

def start():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    start()
