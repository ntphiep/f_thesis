# # Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("ntphiep/viT5_tst_coarse")
# model = AutoModelForSeq2SeqLM.from_pretrained("ntphiep/viT5_tst_coarse")

# def generate_summary(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True).to(model.device)
#     summary_ids = model.generate(**inputs, max_length=256, num_beams=5, early_stopping=True)
#     return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


# sample_text = """
# tôi không hiểu tại sao mọi người lại thích ăn phở đến vậy.
# """

# output = generate_summary(sample_text)
# print("👉 Output:", output)


from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("ntphiep/viT5_tst_coarse")
print(tokenizer("trời hôm nay đẹp thật"))
