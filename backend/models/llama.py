import os
import subprocess

# Ensure Accelerate is installed before using device_map="auto"
try:
    import accelerate
except ImportError:
    subprocess.run(["pip", "install", "accelerate"], check=True)

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import nltk
from huggingface_hub import login

# Load Hugging Face token from environment
hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN is missing! Set it in Render's environment variables.")

# Authenticate with Hugging Face
login(token=hf_token)

# Ensure NLTK is downloaded
nltk.download("punkt")

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer with authentication
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B", use_auth_token=hf_token)
quant_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=quant_config,
    use_auth_token=hf_token
)



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