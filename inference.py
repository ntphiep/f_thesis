from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def model_fn(model_dir, context=None):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    return {"model": model, "tokenizer": tokenizer}

def predict_fn(data, model_artifacts):
    text = data["inputs"]

    tokenizer = model_artifacts["tokenizer"]
    model = model_artifacts["model"]

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(model.device)
    summary_ids = model.generate(**inputs, max_length=256, num_beams=5, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
