from sentence_transformers import SentenceTransformer
import numpy as np

def retrieve_faiss_docs(query, index, document_data, top_k=3):
    """ Retrieve relevant documents using FAISS similarity search. """
    retriever = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_emb = retriever.encode(query, convert_to_numpy=True).astype(np.float32).reshape(1, -1)
    distances, indices = index.search(query_emb, top_k)
    
    results = []
    for i in indices[0]:
        if i < len(document_data):
            doc_text = document_data[i]
            results.append(doc_text)

    return results