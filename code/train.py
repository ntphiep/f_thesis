import argparse
from datasets import load_dataset
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    DataCollatorForSeq2Seq, Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="VietAI/vit5-base")
    parser.add_argument("--dataset_name", type=str)  
    parser.add_argument("--output_dir", type=str, default="/opt/ml/model")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--per_device_train_batch_size", type=int, default=16)
    return parser.parse_args()

def preprocess(example, tokenizer):
    inputs = tokenizer(
        example["input"], max_length=512, padding="max_length", truncation=True
    )
    targets = tokenizer(
        example["target"], max_length=128, padding="max_length", truncation=True
    )
    inputs["labels"] = targets["input_ids"]
    return inputs

def main():
    args = parse_args()

    tokenizer = T5Tokenizer.from_pretrained(args.model_name)
    model = T5ForConditionalGeneration.from_pretrained(args.model_name)

    dataset = load_dataset(args.dataset_name)

    tokenized_datasets = dataset.map(lambda x: preprocess(x, tokenizer), batched=True)

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy="steps",
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        logging_steps=22859,
        predict_with_generate=True,
        save_strategy="steps",
        save_steps=45718,
        eval_steps=22859,
        overwrite_output_dir=True,
        do_train=True,
        do_eval=True,
        save_total_limit=4,
        load_best_model_at_end=True,
        report_to=None,
        group_by_length=True,
        fp16=True,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets.get("test", None),
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )

    trainer.train()
    trainer.save_model(args.output_dir)

if __name__ == "__main__":
    main()
