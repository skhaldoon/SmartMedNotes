from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Split the text into manageable chunks
def split_text_into_chunks(text, max_length=500):
    words = text.split()
    return [" ".join(words[i:i + max_length]) for i in range(0, len(words), max_length)]

# Embed the text
def embed_text(text_chunks):
    return model.encode(text_chunks)

# Load combined text
with open("combined_books.txt", "r", encoding="utf-8") as file:
    combined_text = file.read()

text_chunks = split_text_into_chunks(combined_text)
embeddings = embed_text(text_chunks)
