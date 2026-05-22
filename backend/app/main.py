import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.services.security_service import limiter, rate_limit_handler
from app.routes.line_webhook import router as line_router
from app.routes.admin import router as admin_router


APP_ENV = os.getenv("APP_ENV", "development")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

IS_PRODUCTION = APP_ENV == "production"

app = FastAPI(
    title="LINE OA AI Customer Sentiment Backend",
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
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