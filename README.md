# Crypto Market Intelligence API

> Archived: learning project, no longer maintained.

Async REST API that fetches current crypto prices from CoinGecko, stores each query in PostgreSQL, and runs a sentiment model over headlines. Built to practice FastAPI, async SQLAlchemy and Hugging Face Transformers.

## Endpoints

All routes are under `/api/v1`. Supported symbols: `bitcoin`, `ethereum`, `litecoin` (price and history also accept `btc`, `eth`, `ltc`).

| Method | Path | What it does |
|---|---|---|
| GET | `/` | Health check |
| GET | `/crypto/{symbol}/price` | Fetches price, 24h change, market cap and volume from CoinGecko and saves a row |
| GET | `/crypto/{symbol}/history?limit=50` | Returns the saved rows for that symbol |
| GET | `/crypto/{symbol}/sentiment` | Runs `distilbert-base-uncased-finetuned-sst-2-english` over the headlines and returns the majority label and average score |

Limitation: the headlines are five hardcoded sample sentences per coin in `app/services/sentiment_service.py`, not a live news feed.

## Stack

FastAPI, SQLAlchemy 2.0 (async, asyncpg), PostgreSQL, aiohttp, Hugging Face Transformers (PyTorch), pytest + httpx, Docker. Alembic is configured, but no migration files are committed; tables are created on startup.

## Run locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows; use source venv/bin/activate elsewhere
pip install -r requirements.txt
cp .env.example .env           # set DATABASE_URL, SECRET_KEY, API_V1_STR
uvicorn app.main:app --reload  # docs at http://localhost:8000/docs
```

A `Dockerfile` is included. The first sentiment request downloads the model from Hugging Face.

## Tests

9 async tests in `tests/test_crypto.py`. They use a local SQLite database and mock both the CoinGecko call and the sentiment model, so no network or model download is needed. Run with `pytest`.
