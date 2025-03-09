from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from config import Config
import torch

# LoRA config for efficient fine-tuning
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

def fine_tune_phi3():
    # Load model with 4-bit quantization
    tokenizer = AutoTokenizer.from_pretrained(Config.LLM_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        Config.LLM_MODEL,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    # Load dataset
    dataset = load_dataset("json", data_files="./fine_tuning/orthopedics_dataset.json")["train"]
    
    def format_instruction(sample):
        return f"""<|system|>You are an orthopedic expert.<|end|>
        <|user|>{sample['question']}<|end|>
        <|assistant|>{sample['answer']}<|end|>"""
        
    def tokenize_func(sample):
        return tokenizer(
            format_instruction(sample),
            truncation=True,
            max_length=2048
        )
    
    tokenized_dataset = dataset.map(tokenize_func, batched=False)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=Config.FINE_TUNED_MODEL,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-5,
        fp16=True,
        save_strategy="epoch",
        logging_steps=20,
        optim="paged_adamw_8bit"
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=lambda data: {
            "input_ids": torch.stack([torch.tensor(f["input_ids"]) for f in data]),
            "attention_mask": torch.stack([torch.tensor(f["attention_mask"]) for f in data])
        }
    )
    
    # Start fine-tuning
    trainer.train()
    model.save_pretrained(Config.FINE_TUNED_MODEL)

if __name__ == "__main__":
    fine_tune_phi3()