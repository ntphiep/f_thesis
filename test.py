from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

model_path = './models/coarse/checkpoint-24258'

# Check if local model exists, otherwise use HuggingFace model
if os.path.exists(model_path):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print(f"✓ Loaded local model from {model_path}")
else:
    # Fallback to HuggingFace model
    model_name = "ntphiep/viT5_tst_coarse"
    try:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print(f"✓ Loaded HuggingFace model: {model_name}")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print("Please ensure you have internet access or provide local model files.")
        model = None
        tokenizer = None
 
def generate_summary(text):
    if model is None or tokenizer is None:
        return "Error: No model available. Please check model loading."
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(model.device)
    summary_ids = model.generate(**inputs, max_length=256, num_beams=5, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
 
 
sample_text = """
Bác sĩ Kee Yuan từ Bệnh viện Đại học quốc gia Singapore cũng thừa nhận kỹ thuật mổ nội soi tuyến giáp của các bác sĩ Việt Nam có nhiều ưu điểm vượt trội so với các quốc gia và vùng lãnh thổ khác trên thế giới.
"""

if model is not None and tokenizer is not None:
    output = generate_summary(sample_text)
    print("👉 Output:", output)
else:
    print("👉 Skipping generation due to model loading failure.")