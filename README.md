# Crypto Market Intelligence API

REST API for real-time cryptocurrency market data with AI-powered sentiment analysis.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![Tests](https://img.shields.io/badge/Tests-9%20passed-brightgreen)

## Features

- Real-time crypto prices from CoinGecko API
- Price history persisted in PostgreSQL
- AI sentiment analysis using DistilBERT (HuggingFace)
- Async architecture with FastAPI + SQLAlchemy 2.0
- Full test suite with pytest

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/` | Health check |
| GET | `/api/v1/crypto/{symbol}/price` | Current price + save to DB |
| GET | `/api/v1/crypto/{symbol}/history` | Price history from DB |
| GET | `/api/v1/crypto/{symbol}/sentiment` | AI sentiment analysis |

**Supported symbols:** `bitcoin`, `ethereum`, `litecoin` (also `btc`, `eth`, `ltc`)

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL + SQLAlchemy 2.0** — async database
- **HuggingFace Transformers** — DistilBERT sentiment model
- **aiohttp** — async HTTP client for CoinGecko
- **pytest + httpx** — async testing

## Getting Started
```bash
# Clone and enter
git clone https://github.com/nachixxs/crypto-market-api
cd crypto-market-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run the API
uvicorn app.main:app --reload

# Run tests
pytest
```

## Interactive Docs

Once running, visit `http://localhost:8000/docs` for the Swagger UI.

## Related Projects

- [CryptoLens CLI](https://github.com/nachixxs/cryptolens-cli) — the CLI tool this API is built upon

## Author

**Ignacio Noguerol**
[LinkedIn](https://linkedin.com/in/ignacio-noguerol-54aa942b0) · [GitHub](https://github.com/nachixxs)
