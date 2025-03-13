import logging
import torch
import nltk
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Ensure NLTK punkt is available
nltk.download("punkt")


# ✅ Load Tokenizer and Model Globally
logging.info("🔄 Loading fine-tuned Phi-3 model and tokenizer...")

try:
    tokenizer = AutoTokenizer.from_pretrained("fine_tuned_phi3")
    base_model = AutoModelForCausalLM.from_pretrained(
        "microsoft/phi-3-mini-4k-instruct",
        torch_dtype=torch.float32,  # Use float32 for CPU compatibility
        device_map="cpu",  
        trust_remote_code=True,
        use_cache=False
    )
    
    model = PeftModel.from_pretrained(base_model, "fine_tuned_phi3").merge_and_unload()
    
    logging.info("✅ Model and tokenizer loaded successfully!")

except Exception as e:
    logging.error(f"❌ Error loading model/tokenizer: {e}")
    raise SystemExit("Failed to load model or tokenizer.")

# ✅ Function to generate response
def generate_response(context, user_query, max_new_tokens=50):
    """Generate a response using the fine-tuned Phi-3 model."""
    logging.info("🔄 Generating response using fine-tuned Phi-3...")
    
    try:
        # ✅ Log input details
        logging.info(f"📥 Received query: '{user_query}'")
        logging.info(f"📚 Context length: {len(context.split())} words")
        
        # ✅ Prepare input text
        input_text = f"Context: {context}\nQuery: {user_query}\nAnswer:"
        logging.info("✍️ Tokenizing input...")

        # ✅ Tokenize input
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to("cpu")
        input_ids = inputs["input_ids"][:, -64:]  # ✅ Reduce to last 64 tokens

        # ✅ Log tokenized input details
        logging.info(f"🔢 Tokenized input size: {input_ids.shape}")

        # ✅ Generate response
        logging.info("🤖 Running model inference...")
        with torch.inference_mode():  
            output = model.generate(
                input_ids=input_ids,
                max_new_tokens=20,  
                pad_token_id=tokenizer.eos_token_id,
                num_beams=1,  # ✅ Faster generation
                do_sample=True,
                temperature=0.3,  
                top_p=0.7,  
                return_dict_in_generate=True,  
                output_scores=False,  # ❌ Disabled unnecessary computation
                use_cache=False  
            )

        # ✅ Decode response
        response_text = tokenizer.decode(output.sequences[0], skip_special_tokens=True)
        logging.info(f"📜 Raw generated response: {response_text}")

        # ✅ Extract the final answer
        answer_start = response_text.find("Answer:")
        raw_answer = response_text[answer_start + len("Answer:"):].strip() if answer_start != -1 else response_text.strip()

        # ✅ Format response properly
        try:
            sentences = nltk.sent_tokenize(raw_answer)
            final_answer = " ".join(sentences[: min(len(sentences), 5)])
        except Exception as e:
            logging.error(f"❌ Error in sentence tokenization: {str(e)}")
            final_answer = raw_answer  

        logging.info(f"✅ Final extracted answer: {final_answer}")

        return final_answer

    except Exception as e:
        logging.error(f"❌ Error generating response: {str(e)}")
        return "Error generating response."