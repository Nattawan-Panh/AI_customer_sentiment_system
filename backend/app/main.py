import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.services.security_service import limiter, rate_limit_handler
from app.routes.line_webhook import router as line_router
from app.routes.admin import router as admin_router


APP_ENV = os.getenv("APP_ENV", "development")

IS_PRODUCTION = APP_ENV == "production"

app = FastAPI(
    title="LINE OA AI Customer Sentiment Backend",
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,https://customer-sentiment-syste-b6ca8.web.app"
)

allowed_origins = [
    origin.strip()
    for origin in FRONTEND_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
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


@app.get("/")
@limiter.limit("30/minute")
def root(request: Request):
    return {
        "status": "ok",
        "service": "LINE OA AI Customer Sentiment Backend",
        "version": "1.0.0",
        "environment": APP_ENV
    }


@app.get("/health")
@limiter.limit("60/minute")
def health_check(request: Request):
    return {
        "ok": True,
        "status": "healthy"
    }