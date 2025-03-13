import os
import torch
import nltk
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel  # Import PEFT properly

# Download NLTK tokenizer
nltk.download("punkt")

# ✅ Define fine-tuned model path
fine_tuned_model_path = "./fine_tuned_phi3"  # Ensure this path is correct

# ✅ Load base model first
base_model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-3-mini-4k-instruct",
    torch_dtype=torch.float16,  # Keep float16
    device_map="auto",
    trust_remote_code=True,
    use_cache=False  # Explicitly disable cache
)

# ✅ Attach PEFT adapter
model = PeftModel.from_pretrained(
    base_model,
    fine_tuned_model_path,
    adapter_name="ortho_adapter"
).merge_and_unload() 

# ✅ Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_path)

# ✅ Function to generate response
def generate_response(context, query, max_new_tokens=200):
    """Generate a response using the fine-tuned Phi-3 model."""
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(model.device)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]
    
    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,  # ✅ Explicitly set this
        max_new_tokens=100,
        pad_token_id=tokenizer.eos_token_id,
        num_beams=3,
        do_sample=True
    )

    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract answer after "Answer:"
    answer_start = response_text.find("Answer:")
    raw_answer = response_text[answer_start + len("Answer:"):].strip() if answer_start != -1 else response_text.strip()

    # Ensure the answer ends at a proper sentence boundary
    sentences = nltk.sent_tokenize(raw_answer)
    final_answer = " ".join(sentences[: min(len(sentences), 5)])

    return final_answer
