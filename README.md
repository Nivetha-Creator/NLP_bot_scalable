# NLP Bot Scalable

A FastAPI-based medical information chatbot with TensorFlow intent classification, SQLite persistence, and a built-in web UI.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) or pip

## Setup

1. Clone the repository and enter the project directory.

2. Install dependencies:

```bash
pip install -e .
```

3. Optional: copy the example environment file and adjust values:

```bash
cp .env.example .env
```

The application runs with sensible defaults when no `.env` file is present.

## Run the server

```bash
nlp-bot-scalable
```

Or directly with uvicorn:

```bash
uvicorn nlp_bot_scalable.main:app --host 127.0.0.1 --port 8000 --reload
```

Medical and chat POST endpoints accept JSON request bodies. Configure allowed browser origins with `CORS_ORIGINS` in `.env`.

## Use the application

- **Web UI:** open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) after starting the server
- **API health check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **OpenAPI docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Register an account in the UI, then sign in to use chat and medical services. Chat endpoints require a JWT bearer token returned by `/auth/login`.

## API overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Create a user account |
| `/auth/login` | POST | Sign in and receive a JWT access token |
| `/chat` | POST | Send a chat message (requires `Authorization: Bearer <token>`) |
| `/chat/history` | GET | Retrieve chat history for the authenticated user |
| `/medical/symptoms` | POST | Symptom checker (`{"symptoms": "..."}`) |
| `/medical/medicine` | POST | Medicine information (`{"medicine": "..."}`) |
| `/medical/hospitals` | POST | Hospital finder (`{"city": "..."}`) |
| `/medical/knowledge` | POST | Medical knowledge lookup (`{"topic": "..."}`) |

## Project layout

```
src/nlp_bot_scalable/
  api/          # FastAPI route handlers
  config/       # Settings and database setup
  database/     # SQLAlchemy models and repositories
  frontend/     # Static web UI served by FastAPI
  nlp/          # Intent model, training, and prediction
  services/     # Business logic
models/         # Trained TensorFlow model artifacts
intents.json    # Training intents and responses
```

## Development

Run the existing smoke tests:

```bash
pytest tests/ -v
```

Retrain the intent model (optional):

```bash
python -m nlp_bot_scalable.nlp.trainer
```

Initialize database tables manually (optional):

```bash
python -m nlp_bot_scalable.database.init_db
```
