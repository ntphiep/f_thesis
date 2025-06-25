from transformers import T5Tokenizer, T5ForConditionalGeneration
from datasets import load_dataset
import torch
import math

model_path = './models/formal'+ '/checkpoint-24258'

# Load model và tokenizer fine-tuned
model = T5ForConditionalGeneration.from_pretrained(model_path)  # Đường dẫn model đã fine-tuned
tokenizer = T5Tokenizer.from_pretrained(model_path)

# Load dataset để đánh giá (dùng dataset của mình hoặc dataset đã có sẵn)
dataset = load_dataset("your_dataset", split="test")  # Hoặc sử dụng dataset cụ thể

# Tokenize input và output
inputs = tokenizer(dataset['input_column'], return_tensors='pt', padding=True, truncation=True)
labels = tokenizer(dataset['output_column'], return_tensors='pt', padding=True, truncation=True).input_ids

# Cẩn thận với padding
labels[labels == tokenizer.pad_token_id] = -100  # Đánh dấu token padding là -100 để ignore trong tính loss

# Dự đoán và tính loss
model.eval()
with torch.no_grad():
    outputs = model(**inputs, labels=labels)
    loss = outputs.loss

# Tính Perplexity
perplexity = math.exp(loss.item())
print(f"Perplexity: {perplexity}")
