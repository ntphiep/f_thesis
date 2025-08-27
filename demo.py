from datasets import load_dataset
from transformers import pipeline
import evaluate
import sacrebleu

# --- Config ---
dataset_name = "ntphiep/vit5-tst-data-formal"   # thay bằng tên dataset thật
model_name = "ntphiep/viT5_tst_formal"       # thay bằng tên model thật
num_samples = 30

# Load dataset
dataset = load_dataset(dataset_name, split="train")

# Lấy 30 câu mẫu
samples = dataset.select(range(num_samples))
inputs = samples["input"]
references = samples["target"]

# Load model pipeline
generator = pipeline("text2text-generation", model=model_name)

# Sinh output
predictions = [
    generator(text, max_length=128, clean_up_tokenization_spaces=True)[0]['generated_text']
    for text in inputs
]

# Load metrics
rouge = evaluate.load("rouge")
bleu = evaluate.load("bleu")
meteor = evaluate.load("meteor")
bertscore = evaluate.load("bertscore")

# Compute metrics
rouge_result = rouge.compute(predictions=predictions, references=references)
# bleu_result = bleu.compute(
#     predictions=[p.split() for p in predictions],
#     references=[[r.split()] for r in references]
# )
bleu_result = sacrebleu.corpus_bleu(predictions, [references])
meteor_result = meteor.compute(predictions=predictions, references=references)
bertscore_result = bertscore.compute(predictions=predictions, references=references, lang="vi")

# Print results
print("=== Evaluation Results ===")
print(f"ROUGE-1: {rouge_result['rouge1']:.4f}")
print(f"ROUGE-2: {rouge_result['rouge2']:.4f}")
print(f"ROUGE-L: {rouge_result['rougeL']:.4f}")
print(f"BLEU: {bleu_result.score}")
print(f"METEOR: {meteor_result['meteor']:.4f}")
print(f"BERTScore F1: {sum(bertscore_result['f1'])/len(bertscore_result['f1']):.4f}")
