from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained("./gpt2-finetuned")
tokenizer = GPT2Tokenizer.from_pretrained("./gpt2-finetuned")

# Input text
input_text = "How do medical professionals fix a broken arm? "
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate response
outputs = model.generate(
    input_ids=input_ids,
    max_length=150,                # Increased max length
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.5,               # Add some randomness
    top_k=50,                      # Top-k sampling
    top_p=0.95,                    # Top-p sampling
    no_repeat_ngram_size=2,        # Avoid repetition
    early_stopping=True            # Stop naturally
)

# Decode and print the output
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
