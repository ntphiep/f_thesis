import torch
import math
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sacrebleu
import evaluate
from sklearn.metrics import pairwise_distances

MODELS = {}

for model_name in ["casual", "chinese", "coarse", "formal"]:
    model_path = f"./models/{model_name}/checkpoint-24258"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    MODELS[model_name] = (model, tokenizer)
 
def generate_summary(text, model_name, top_p=0.7):
    model, tokenizer = MODELS[model_name]

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(model.device)
    summary_ids = model.generate(
        **inputs, 
        max_length=256, 
        num_beams=5, 
        top_p=top_p,
        early_stopping=True,
        do_sample=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
 


print(MODELS)