from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from nlp_bot_scalable.api.auth_routes import router as auth_router
from nlp_bot_scalable.api.chat_routes import router as chat_router
from nlp_bot_scalable.api.medical_routes import router as medical_router
from nlp_bot_scalable.config.settings import settings

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

app = FastAPI(
    title=settings.app_name,
    description="Scalable NLP Chatbot API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(medical_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend",
)
