import json
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model

MODEL_NAME = "gpt2"
TRAIN_FILE = "ft_data.jsonl"
OUTPUT_DIR = "my_friend_ft"

def load_jsonl_dataset(path):
    return load_dataset("json", data_files=path, split="train")

def format_example(example):
    return {"text": example["prompt"] + example["completion"]}

def tokenize(tokenizer, example):
    out = tokenizer(
        example["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )
    out["labels"] = out["input_ids"].copy()
    return out

def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        load_in_8bit=True,
        device_map="auto"
    )

    lora_cfg = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["c_attn", "c_proj"],
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_cfg)

    raw = load_jsonl_dataset(TRAIN_FILE)
    ds = raw.map(format_example)
    ds = ds.map(lambda e: tokenize(tokenizer, e), batched=True)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        save_strategy="epoch",
        logging_steps=20,
        learning_rate=2e-4,
        num_train_epochs=3,
        warmup_steps=80,
        fp16=True,
        optim="paged_adamw_8bit",
        report_to=[]
    )

    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=args,
        train_dataset=ds,
        data_collator=data_collator
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Training done. Model saved to:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
