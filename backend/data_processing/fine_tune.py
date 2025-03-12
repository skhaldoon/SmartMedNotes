#TRANING THE LLM MODEL
# Enable internet access in Kaggle settings first!
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Configuration
model_name = "microsoft/Phi-3-mini-4k-instruct"
output_dir = "/kaggle/working/fine_tuned_phi3"
dataset_paths = [
    "/kaggle/working/processed_data/orthopedic_qa.json",
    "/kaggle/working/processed_data/orthopedic_case_queries.json"
]

# 1. 4-bit Quantization Config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# 2. Load Model
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# 3. Prepare for PEFT
model = prepare_model_for_kbit_training(model)

# 4. LoRA Config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

# 5. Dataset Formatting
def format_instruction(examples):
    formatted_texts = []
    for content in examples["content"]:
        if isinstance(content, list):
            content = " ".join(content)
        if "Q: " in content and "A: " in content:
            q_part = content.split("Q: ")[1]
            question = q_part.split("A: ")[0].strip()
            answer = q_part.split("A: ")[1].strip()
        else:
            question = content
            answer = ""
        formatted_texts.append(
            f"<|user|>\n{question}<|end|>\n<|assistant|>\n{answer}<|end|>\n"
        )
    return {"text": formatted_texts}

# 6. Load and process dataset
dataset = load_dataset("json", data_files=dataset_paths, split="train")
dataset = dataset.map(format_instruction, batched=True)

# 7. CORRECTED Tokenization with labels
def tokenize_function(examples):
    tokenized = tokenizer(
        examples["text"],
        truncation=True,
        max_length=1024,
        padding="max_length",
        add_special_tokens=True
    )
    # Add labels for language modeling
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# 8. Data Collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # For causal language modeling
)

# 9. Training Arguments
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    optim="paged_adamw_8bit",
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none",
    gradient_checkpointing=True
)

# 10. Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator  # Add data collator
)

# 11. Start Training
trainer.train()

# 12. Save Model
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print("✅ Training completed successfully!")