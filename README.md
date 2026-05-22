# LINE OA AI Customer Sentiment & Auto-Reply System — Full Production Version

โปรเจกต์นี้รวมโค้ดเดิมและโค้ดใหม่สำหรับ Production ครบชุด:

- LINE OA Webhook
- FastAPI Backend
- Firebase Realtime Database
- Firebase Hosting Dashboard
- Firebase Auth Admin Login
- Email Notification เมื่อ High Risk / Pending Review
- Groq API แทน Ollama local
- Auto Reply / Human Review
- Error Logging ทุกขั้นตอน
- Render / Docker deployment
- Training starter สำหรับ WangchanBERTa

## รัน Backend ใน VS Code

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install fastapi
pip install uvicorn
pip install python-dotenv
pip install firebase-admin
pip install requests
pip install pydantic
pip install pandas
pip install scikit-learn
pip install slowapi
copy .env.example .env
python -m uvicorn app.main:app --reload --port 8000
```

## ทดสอบ Mock LINE

```powershell
Invoke-RestMethod `
-Uri "http://127.0.0.1:8000/line/mock" `
-Method POST `
-ContentType "application/json" `
-Body '{"line_user_id":"mock-user","text":"ส่งของช้ามาก อยากคืนเงิน"}'
```

## Deploy Backend ไป Render

ใช้ไฟล์ `backend/render.yaml` หรือ Start Command:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Deploy Frontend ไป Firebase Hosting

```bash
cd frontend
firebase login
firebase init hosting
firebase deploy
```

## ตั้งค่า Firebase

1. เปิด Realtime Database
2. เปิด Firebase Auth แบบ Email/Password
3. เปิด Firebase Hosting
4. ใส่ Web config ใน `frontend/public/js/firebase-config.js`
5. วาง Service Account ที่ `backend/serviceAccountKey.json` หรือใช้ `FIREBASE_SERVICE_ACCOUNT_JSON` บน Cloud
6. นำ rules จาก `docs/firebase-database-rules.json` ไปใส่ใน Firebase Realtime Database Rules

## ตั้งค่า Groq API

ใส่ใน `.env` และ Render Environment:

```env
GROQ_API_KEY=your_groq_key
GROQ_MODEL=llama-3.1-8b-instant
```
