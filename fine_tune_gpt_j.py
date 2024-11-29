from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
import torch


model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

dataset = load_dataset('json', data_files=r'C:\Users\admin\l7erf-bot\fine_tune_dataset.jsonl', split='train')
print(f"Loaded dataset: {dataset}")
print(f"First few entries of dataset: {dataset[:5]}")  

def tokenize(batch):
    return tokenizer(batch["prompt"], padding="max_length", truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize, batched=True)
print(f"Tokenized dataset: {tokenized_dataset[:5]}") 

training_args = TrainingArguments(
    output_dir="./fine_tuned_gpt_j",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    learning_rate=5e-5,
    logging_dir="./logs",
    logging_steps=10,  
    save_steps=100,   
    evaluation_strategy="steps",  
    logging_level="debug", 
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

try:
    print("Training started...")
    trainer.train()
except Exception as e:
    print(f"An error occurred during training: {e}")

model.save_pretrained(r"C:\Users\admin\l7erf-bot\fine_tuned_gpt_j")
tokenizer.save_pretrained(r"C:\Users\admin\l7erf-bot\fine_tuned_gpt_j")

print("Fine-tuning complete, model saved.")
