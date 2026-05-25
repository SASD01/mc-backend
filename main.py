import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import api_router

_ENV = os.getenv("ENVIRONMENT", "production")

_ALLOWED_ORIGINS = (
    [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
    if _ENV == "production"
    else ["*"]
)

app = FastAPI(
    title="MediConnect API",
    version="1.0.0",
    docs_url="/docs" if _ENV != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "ok"}


@app.get("/debug/env", include_in_schema=False)
def debug_env():
    """Temporary endpoint to diagnose Vercel env vars. REMOVE after fixing."""
    def mask(val):
        if not val:
            return "NOT_SET"
        if len(val) < 10:
            return f"{val[:2]}...({len(val)} chars)"
        return f"{val[:6]}...{val[-4:]} ({len(val)} chars)"

    raw_url = os.getenv("PUBLIC_SUPABASE_URL")
    raw_anon = os.getenv("PUBLIC_SUPABASE_ANON_KEY")
    raw_service = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    return {
        "PUBLIC_SUPABASE_URL": raw_url or "NOT_SET",
        "PUBLIC_SUPABASE_ANON_KEY": mask(raw_anon),
        "SUPABASE_SERVICE_ROLE_KEY": mask(raw_service),
        "all_env_keys_containing_supa": [
            k for k in os.environ.keys()
            if "supa" in k.lower() or "supabase" in k.lower()
        ],
    }

from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    import traceback
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "trace": traceback.format_exc()},
    )
