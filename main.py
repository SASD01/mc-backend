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

from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.errors(), "body": exc.body},
    )
