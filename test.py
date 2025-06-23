from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = './models/coarse'+ '/checkpoint-24258'
 
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
 
def generate_summary(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(model.device)
    summary_ids = model.generate(**inputs, max_length=256, num_beams=5, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
 
 
sample_text = """
Bác sĩ Kee Yuan từ Bệnh viện Đại học quốc gia Singapore cũng thừa nhận kỹ thuật mổ nội soi tuyến giáp của các bác sĩ Việt Nam có nhiều ưu điểm vượt trội so với các quốc gia và vùng lãnh thổ khác trên thế giới.
"""
output = generate_summary(sample_text)
print("👉 Output:", output)