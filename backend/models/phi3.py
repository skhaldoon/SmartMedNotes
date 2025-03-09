import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import Config
import nltk

nltk.download("punkt")

def load_phi3():
    """Load Phi-3 with CPU optimizations"""
    tokenizer = AutoTokenizer.from_pretrained(Config.LLM_MODEL)
    
    model = AutoModelForCausalLM.from_pretrained(
        Config.LLM_MODEL,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    
    if os.path.exists(Config.FINE_TUNED_MODEL):
        model.load_adapter(Config.FINE_TUNED_MODEL)
        
    return tokenizer, model

tokenizer, model = load_phi3()

def generate_response(context, query, max_new_tokens=200):
    """Generate response with CPU optimizations"""
    prompt = f"""<|system|>
    You are an orthopedic expert. Use this context: {context}
    Answer the query precisely and end properly.<|end|>
    <|user|>{query}<|end|>
    <|assistant|>"""
    
    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_response.split("<|assistant|>")[-1].strip()
    
    # Ensure proper sentence endings
    sentences = nltk.sent_tokenize(response)
    if sentences and not sentences[-1].endswith(('.', '!', '?')):
        sentences[-1] += '.'
        
    return ' '.join(sentences[:4])  # Return first 4 sentences max