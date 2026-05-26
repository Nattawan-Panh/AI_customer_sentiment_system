import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.services.security_service import limiter, rate_limit_handler
from app.routes.line_webhook import router as line_router
from app.routes.admin import router as admin_router


APP_ENV = os.getenv("APP_ENV", "development")
IS_PRODUCTION = APP_ENV == "production"

FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,https://customer-sentiment-syste-b6ca8.web.app,https://customer-sentiment-syste-b6ca8.firebaseapp.com"
)

allowed_origins = [
    origin.strip()
    for origin in FRONTEND_ORIGINS.split(",")
    if origin.strip()
]

app = FastAPI(
    title="LINE OA AI Customer Sentiment Backend",
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "customer-sentiment-backend"
    }

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    line_router,
    prefix="/line",
    tags=["LINE OA Webhook"]
)

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)


