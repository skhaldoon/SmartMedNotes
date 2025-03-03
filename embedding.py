import json
import os
from sentence_transformers import SentenceTransformer

def generate_embeddings(data_path, model_name="sentence-transformers/all-MiniLM-L6-v2", batch_size=32):
    """
    Generate embeddings for the dataset using SentenceTransformer with batch processing.
    """
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found - {data_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format - {data_path}")
        return None

    model = SentenceTransformer(model_name)

    texts = []
    for item in data:
        if 'content' in item:
            texts.append(item['content'])
        elif 'Question' in item and 'Answer' in item:
            texts.append(item['Question'] + " " + item['Answer'])
        else:
            print(f"Warning: Skipping an entry in {data_path} due to missing keys.")

    if not texts:
        print(f"Error: No valid text data found in {data_path}")
        return None

    embeddings = model.encode(texts, convert_to_tensor=False, batch_size=batch_size)

    # Store results
    results = []
    for i, item in enumerate(data):
        entry = {"embedding": embeddings[i].tolist()}
        if 'content' in item:
            entry["content"] = item['content']
        else:
            entry["Question"] = item.get('Question', "")
            entry["Answer"] = item.get('Answer', "")
        results.append(entry)

    return results

def save_embeddings(embeddings, input_path):
    """
    Save embeddings to a JSON file in the /kaggle/working/ directory.
    """
    if embeddings is None:
        print(f"Skipping saving embeddings for {input_path} due to an error.")
        return

    output_file = os.path.join("/kaggle/working/", os.path.basename(input_path).replace('.json', '_embeddings.json'))

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings, f, indent=4, ensure_ascii=False)
        print(f"Saved embeddings to {output_file}")
    except Exception as e:
        print(f"Error saving embeddings file {output_file}: {e}")

if __name__ == "__main__":
    json_files = [
        "/kaggle/working/MayoClinic.json",
        "/kaggle/working/Osteoporosis-MayoClinic.json",
        "/kaggle/working/speakingTree-Jayant.json",
        "/kaggle/working/orthopedics.json",
        "/kaggle/working/info.json",
        "/kaggle/working/orthopedic_qa.json",
        "/kaggle/working/orthopedic_case_queries.json"
    ]

    for json_file in json_files:
        print(f"Processing: {json_file}")
        embeddings = generate_embeddings(json_file)
        save_embeddings(embeddings, json_file)
