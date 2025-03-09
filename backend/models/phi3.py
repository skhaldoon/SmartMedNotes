import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from huggingface_hub import login
import nltk

nltk.download("punkt")

# Quantization config for memory efficiency
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

def load_phi3():
    """Load Phi-3 with 4-bit quantization"""
    tokenizer = AutoTokenizer.from_pretrained(Config.LLM_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        Config.LLM_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Load fine-tuned adapter if exists
    if os.path.exists(Config.FINE_TUNED_MODEL):
        model = PeftModel.from_pretrained(model, Config.FINE_TUNED_MODEL)
        model = model.merge_and_unload()
        
    return tokenizer, model

tokenizer, model = load_phi3()

def generate_response(context, query, max_new_tokens=250):
    """Generate response with proper sentence boundaries"""
    prompt = f"""<|system|>
    You are an orthopedic expert. Use this context: {context}
    Answer the query precisely and end properly.<|end|>
    <|user|>{query}<|end|>
    <|assistant|>"""
    
    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False).to(model.device)
    
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
    if sentences:
        last_sentence = sentences[-1]
        if not last_sentence.endswith(('.', '!', '?')):
            sentences[-1] = last_sentence + '.'
            
    return ' '.join(sentences[:5])