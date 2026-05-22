import os
import json
import numpy as np
import pandas as pd
import torch

from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
    EarlyStoppingCallback
)

DATASET_FILE = "dataset.csv"

MODEL_NAME = "airesearch/wangchanberta-base-att-spm-uncased"

CHECKPOINT_DIR = "checkpoints"
FINAL_MODEL_DIR = "wangchanberta_sentiment_model"

MAX_LENGTH = 128
RANDOM_STATE = 42

LABEL2ID = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}

ID2LABEL = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

def load_data():
    if not os.path.exists(DATASET_FILE):
        raise FileNotFoundError(
            f"ไม่พบไฟล์ {DATASET_FILE} กรุณารัน prepare_dataset.py ก่อน"
        )

    df = pd.read_csv(DATASET_FILE)

    df = df.dropna(subset=["text", "label"])
    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(str).str.lower().str.strip()

    df = df[df["label"].isin(LABEL2ID.keys())]
    df["label"] = df["label"].map(LABEL2ID)

    df = df.drop_duplicates(subset=["text"])
    df = df.reset_index(drop=True)

    if len(df) < 30:
        raise ValueError("ข้อมูลน้อยเกินไปสำหรับการ train ควรมีข้อมูลมากกว่านี้")

    print("Dataset size:", len(df))
    print("Label distribution:")
    print(df["label"].value_counts())

    return df

def split_data(df):
    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df["label"],
        random_state=RANDOM_STATE
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        stratify=temp_df["label"],
        random_state=RANDOM_STATE
    )

    print("Train:", len(train_df))
    print("Validation:", len(val_df))
    print("Test:", len(test_df))

    return train_df, val_df, test_df

def create_hf_dataset(train_df, val_df, test_df, tokenizer):
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    test_dataset = Dataset.from_pandas(test_df)

    def tokenize_function(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH
        )

    train_dataset = train_dataset.map(tokenize_function, batched=True)
    val_dataset = val_dataset.map(tokenize_function, batched=True)
    test_dataset = test_dataset.map(tokenize_function, batched=True)

    keep_columns = ["input_ids", "attention_mask", "label"]

    train_dataset = train_dataset.remove_columns(
        [col for col in train_dataset.column_names if col not in keep_columns]
    )

    val_dataset = val_dataset.remove_columns(
        [col for col in val_dataset.column_names if col not in keep_columns]
    )

    test_dataset = test_dataset.remove_columns(
        [col for col in test_dataset.column_names if col not in keep_columns]
    )

    return train_dataset, val_dataset, test_dataset

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    accuracy = accuracy_score(labels, predictions)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="weighted",
        zero_division=0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

def train():
    df = load_data()
    train_df, val_df, test_df = split_data(df)

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        use_fast=False
    )

    train_dataset, val_dataset, test_dataset = create_hf_dataset(
        train_df,
        val_df,
        test_df,
        tokenizer
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir=CHECKPOINT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_dir="logs",
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
        report_to="none",
        fp16=torch.cuda.is_available()
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        callbacks=[
            EarlyStoppingCallback(early_stopping_patience=2)
        ]
    )

    trainer.train()

    print("\nEvaluating on test set...")
    test_result = trainer.evaluate(test_dataset)
    print(test_result)

    trainer.save_model(FINAL_MODEL_DIR)
    tokenizer.save_pretrained(FINAL_MODEL_DIR)

    with open(os.path.join(FINAL_MODEL_DIR, "label_map.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "label2id": LABEL2ID,
                "id2label": ID2LABEL
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    with open(os.path.join(FINAL_MODEL_DIR, "test_result.json"), "w", encoding="utf-8") as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)

    print("\n==============================")
    print("Training completed.")
    print("Model saved to:", FINAL_MODEL_DIR)
    print("==============================")

if __name__ == "__main__":
    train()