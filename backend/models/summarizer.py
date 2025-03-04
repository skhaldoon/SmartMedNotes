from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sum_tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
sum_model = T5ForConditionalGeneration.from_pretrained("t5-small").to(device).eval()

def summarize_context(context):
    """ Summarize retrieved documents to make context concise. """
    if not context:
        return ""
    
    input_text = "summarize: " + context
    input_ids = sum_tokenizer.encode(input_text, return_tensors="pt").to(device)
    summary_ids = sum_model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    
    return sum_tokenizer.decode(summary_ids[0], skip_special_tokens=True)