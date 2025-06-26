import flask
from flask import Flask
from flask import request
import json
import datetime
import os
import re
import secrets
import math
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sacrebleu
import evaluate

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
    results = bertscore.compute(predictions=predictions, references=references, lang="vi")
    return sum((results["f1"])) / len(results["f1"]) if results["f1"] else 0.0

# METEOR
def evaluate_meteor(predictions, references):
    meteor = evaluate.load("meteor")
    results = meteor.compute(predictions=predictions, references=references)
    return results


MODELS = {}
app = Flask(__name__)

with open("../config.json", "r") as f:
    configuration = json.loads(f.read())
    OUTPUT_DIR = configuration["output_dir"]

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
 


@app.route('/get_strap_doc', methods=['GET'])
def get_strap_doc():
    strap_key = request.args['id']

    queue_number = 0

    with open(OUTPUT_DIR + "/generated_outputs/queue/queue.txt", "r") as f:
        for i, line in enumerate(f):
            if strap_key == line.strip():
                queue_number = i + 1

    with open(OUTPUT_DIR + "/generated_outputs/inputs/%s/metadata.json" % strap_key, "r") as f:
        metadata = json.loads(f.read())

    if queue_number == 0:
        with open(OUTPUT_DIR + "/generated_outputs/final/%s.json" % strap_key, 'r') as f:
            strap_data = json.loads(f.read())
        status = None
    else:
        strap_data = None
        status = "processing input..."

    response = flask.jsonify({
        "output_data": strap_data,
        "queue_number": queue_number,
        "settings": metadata["settings"],
        "input_text": metadata["input_text"],
        "status": status,
        "target_style": metadata["target_style"],
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/request_strap_doc', methods=['POST'])
def request_strap_doc():
    form_data = json.loads(request.data.decode('utf-8'))


    output = generate_summary(
        form_data["input_text"],
        str(form_data["target_style"]).lower(),
        top_p=form_data["top_p_style"]
    )
    
    bleu_score = evaluate_bleu([output], [form_data["input_text"]])
    rouge_score = evaluate_rouge([output], [form_data["input_text"]])
    bertscore = evaluate_bertscore([output], [form_data["input_text"]])
    meteor_score = evaluate_meteor([output], [form_data["input_text"]])


    response = flask.jsonify({
        "input_text": form_data["input_text"],
        "output_text": output,
        "bleu_score": bleu_score,
        "rouge_score": rouge_score["rougeLsum"],
        "bertscore": bertscore,
        "meteor_score": meteor_score["meteor"],
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
