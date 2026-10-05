from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.nlp_bot_scalable.api.auth_routes import router as auth_router
from src.nlp_bot_scalable.api.chat_routes import router as chat_router
from src.nlp_bot_scalable.api.medical_routes import router as medical_router


app = FastAPI(
    title="NLP Chatbot API",
    description="Scalable NLP Chatbot API",
    version="1.0.0"
)


# Include API routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(medical_router)


# Allow frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "NLP Chatbot API is running!"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }