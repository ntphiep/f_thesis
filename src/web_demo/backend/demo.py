import torch
import math
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sacrebleu
import evaluate
from sklearn.metrics import pairwise_distances
from fastapi import FastAPI

app = FastAPI()
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
 



# BLEU
def evaluate_bleu(predictions, references):
    bleu = sacrebleu.corpus_bleu(predictions, [references])
    return bleu.score

# ROUGE
def evaluate_rouge(predictions, references):
    rouge = evaluate.load("rouge")
    results = rouge.compute(predictions=predictions, references=references)
    return results

# BERTScore 
def evaluate_bertscore(predictions, references):
    bertscore = evaluate.load("bertscore")
    results = bertscore.compute(predictions=predictions, references=references, lang="vi", rescale_with_baseline=True)
    return sum((results["f1"]) / len(results["f1"])) if results["f1"] else 0.0

# METEOR
def evaluate_meteor(predictions, references):
    meteor = evaluate.load("meteor")
    results = meteor.compute(predictions=predictions, references=references)
    return results


input_text = [
    "Việc chữ sida trùng với tên gọi căn bệnh SIDA AIDS chỉ là ngẫu nhiên .",
    "Tình hình đó buộc McAthur phải ra lệnh cho quân Mỹ và quân Nam Triều Tiên rút lui toàn bộ .",
    "Bệnh dịch này, hễ xâm nhập vào trư tộc, tốc độ lây lan cực kỳ nhanh chóng, không phân biệt chủng loại, một khi nhiễm bệnh, tỷ lệ tử vong đạt đến bách phần bách.",
    "Tại Malaysia, yếu tố sắc tộc có ảnh hưởng đáng kể đến hoạt động chính trị, thể hiện qua việc nhiều chính đảng được xây dựng dựa trên nền tảng dân tộc.",
    "Quân nổi dậy của thằng Castro nó chiếm mẹ thủ đô ngày 3 tháng 1 năm 1959 rồi."
    
]
output_text = [generate_summary(i, "casual") for i in input_text]



# 3. Đánh giá bằng BERTScore
bertscore = evaluate.load("bertscore")
bert_score = bertscore.compute(predictions=output_text, references=input_text, lang="vi")
print("BERTScore (F1):", sum(bert_score['f1']) / len(bert_score['f1']))