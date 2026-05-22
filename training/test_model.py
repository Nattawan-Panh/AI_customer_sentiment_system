import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "wangchanberta_sentiment_model"

ID2LABEL = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

def predict_sentiment(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        padding=True
    )

    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)
        prediction_id = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][prediction_id].item()

    return {
        "text": text,
        "sentiment": ID2LABEL[prediction_id],
        "confidence": round(confidence, 4)
    }

if __name__ == "__main__":
    examples = [
        "สินค้าดีมาก ชอบมากค่ะ",
        "บริการแย่มาก ไม่ประทับใจเลย",
        "ได้รับสินค้าแล้วค่ะ",
        "ตอบช้ามาก เสียความรู้สึก",
        "คุณภาพโอเค ใช้งานได้ปกติ"
    ]

    for text in examples:
        result = predict_sentiment(text)
        print(result)