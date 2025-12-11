from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def model_fn(model_dir, context=None):
    # Enable model optimization if CUDA is available
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir).to(device)
    
    # Enable model evaluation mode for inference (disables dropout, etc.)
    model.eval()
    
    # Enable torch.no_grad() context for inference to reduce memory usage
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    return {"model": model, "tokenizer": tokenizer}

def predict_fn(data, model_artifacts):
    text = data["inputs"]

    tokenizer = model_artifacts["tokenizer"]
    model = model_artifacts["model"]

    # Use torch.no_grad() to disable gradient computation for inference
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(model.device)
        summary_ids = model.generate(**inputs, max_length=256, num_beams=5, early_stopping=True)
    
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
