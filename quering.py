import numpy as np

def find_most_relevant_chunk(query, text_chunks, embeddings, model):
    query_embedding = model.encode([query])
    similarities = np.dot(embeddings, query_embedding.T).flatten()
    most_relevant_index = np.argmax(similarities)
    return text_chunks[most_relevant_index]


