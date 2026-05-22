import os
import re
import glob
import pandas as pd

RAW_DATASET_DIR = "raw_datasets"
OUTPUT_FILE = "dataset.csv"

TEXT_COLUMNS = [
    "text",
    "comment",
    "comments",
    "review",
    "reviews",
    "content",
    "sentence",
    "message",
    "tweet",
    "thai_text",
    "body",
    "description"
]

LABEL_COLUMNS = [
    "label",
    "sentiment",
    "class",
    "category",
    "target",
    "rating",
    "score",
    "stars"
]

LABEL_MAP = {
    "positive": "positive",
    "pos": "positive",
    "good": "positive",
    "happy": "positive",
    "บวก": "positive",
    "ดี": "positive",
    "พอใจ": "positive",

    "neutral": "neutral",
    "neu": "neutral",
    "normal": "neutral",
    "กลาง": "neutral",
    "ปานกลาง": "neutral",
    "เฉยๆ": "neutral",

    "negative": "negative",
    "neg": "negative",
    "bad": "negative",
    "sad": "negative",
    "angry": "negative",
    "ลบ": "negative",
    "แย่": "negative",
    "ไม่พอใจ": "negative"
}

def clean_text(text):
    text = str(text).strip()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"(.)\1{3,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def find_column(df, possible_columns):
    lower_columns = {col.lower().strip(): col for col in df.columns}

    for col in possible_columns:
        if col.lower() in lower_columns:
            return lower_columns[col.lower()]

    return None

def normalize_label(value):
    if pd.isna(value):
        return None

    raw = str(value).strip().lower()

    if raw in LABEL_MAP:
        return LABEL_MAP[raw]

    try:
        number = float(raw)

        if number >= 4:
            return "positive"
        elif number == 3:
            return "neutral"
        elif number <= 2:
            return "negative"

    except ValueError:
        pass

    return None

def read_dataset_safely(file_path):

    encodings = ["utf-8", "utf-8-sig", "cp874", "tis-620", "latin1"]

    extension = os.path.splitext(file_path)[1].lower()

    last_error = None

    for enc in encodings:

        try:

            print(f"Trying {file_path} with {enc}")

            # =========================
            # CSV
            # =========================
            if extension == ".csv":

                return pd.read_csv(
                    file_path,
                    encoding=enc,
                    on_bad_lines="skip"
                )

            # =========================
            # TSV
            # =========================
            elif extension == ".tsv":

                return pd.read_csv(
                    file_path,
                    encoding=enc,
                    sep="\t",
                    on_bad_lines="skip"
                )

            # =========================
            # TXT
            # =========================
            elif extension == ".txt":

                filename = os.path.basename(file_path)

                # ข้ามไฟล์ label
                if "_label" in filename.lower():
                    return None

                # =====================
                # หาไฟล์ label คู่กัน
                # =====================
                base_name = filename.replace(".txt", "")

                possible_label_files = [
                    os.path.join(
                        RAW_DATASET_DIR,
                        base_name + "_label.txt"
                    ),
                    os.path.join(
                        RAW_DATASET_DIR,
                        base_name.replace("_train", "_train_label") + ".txt"
                    ),
                    os.path.join(
                        RAW_DATASET_DIR,
                        base_name.replace("_test", "_test_label") + ".txt"
                    )
                ]

                label_file = None

                for lf in possible_label_files:
                    if os.path.exists(lf):
                        label_file = lf
                        break

                # =====================
                # อ่านข้อความ
                # =====================
                with open(
                    file_path,
                    "r",
                    encoding=enc,
                    errors="ignore"
                ) as f:

                    texts = [
                        line.strip()
                        for line in f.readlines()
                        if line.strip()
                    ]

                # =====================
                # อ่าน label
                # =====================
                if label_file:

                    with open(
                        label_file,
                        "r",
                        encoding=enc,
                        errors="ignore"
                    ) as f:

                        labels = [
                            line.strip()
                            for line in f.readlines()
                            if line.strip()
                        ]

                    min_len = min(len(texts), len(labels))

                    df = pd.DataFrame({
                        "text": texts[:min_len],
                        "label": labels[:min_len]
                    })

                    return df

                # =====================
                # ไม่มี label
                # =====================
                else:

                    return pd.DataFrame({
                        "text": texts
                    })

        except Exception as e:

            last_error = e
            print(f"Failed with {enc}: {e}")

            continue

    raise ValueError(
        f"ไม่สามารถอ่านไฟล์ได้: {file_path} | error: {last_error}"
    )

def process_file(file_path):

    print(f"\nReading: {file_path}")

    df = read_dataset_safely(file_path)

    if df is None:
        return None

    text_col = find_column(df, TEXT_COLUMNS)
    label_col = find_column(df, LABEL_COLUMNS)

    # กรณี dataframe มี text label อยู่แล้ว
    if "text" in df.columns and "label" in df.columns:
        text_col = "text"
        label_col = "label"

    if text_col is None or label_col is None:

        print("Skipped file because required columns were not found.")
        print("Columns:", list(df.columns))
        print(df.head())

        return None

    new_df = df[[text_col, label_col]].copy()

    new_df.columns = ["text", "label"]

    new_df["text"] = new_df["text"].apply(clean_text)

    new_df["label"] = new_df["label"].apply(normalize_label)

    new_df = new_df.dropna(subset=["text", "label"])

    new_df = new_df[
        new_df["text"].str.len() >= 3
    ]

    print("Usable rows:", len(new_df))

    print(new_df["label"].value_counts())

    return new_df

def main():
    csv_files = glob.glob(os.path.join(RAW_DATASET_DIR, "*.csv"))

    txt_files = glob.glob(os.path.join(RAW_DATASET_DIR, "*.txt"))

    tsv_files = glob.glob(os.path.join(RAW_DATASET_DIR, "*.tsv"))

    all_files = csv_files + txt_files + tsv_files

    if not all_files:
        raise FileNotFoundError(
            f"ไม่พบ dataset ในโฟลเดอร์ {RAW_DATASET_DIR}"
        )

    all_datasets = []

    for file_path in all_files:
        processed_df = process_file(file_path)

        if processed_df is not None and len(processed_df) > 0:
            all_datasets.append(processed_df)

    if not all_datasets:
        raise ValueError("ไม่พบ dataset ที่ใช้งานได้")

    final_df = pd.concat(all_datasets, ignore_index=True)

    # ลบข้อความซ้ำ
    final_df = final_df.drop_duplicates(subset=["text"])

    # สับลำดับข้อมูลใหม่ โดยไม่ลดจำนวนข้อมูล
    final_df = final_df.sample(
        #frac=1,
        random_state=42,
        n=5000
    ).reset_index(drop=True)

    final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("\n==============================")
    print("Saved:", OUTPUT_FILE)
    print("Total rows:", len(final_df))
    print("Label distribution:")
    print(final_df["label"].value_counts())
    print("==============================")

if __name__ == "__main__":
    main()