import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient


# ── Health Check ──────────────────────────────────────────────────────────────

async def test_health_check(client: AsyncClient):
    response = await client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ── Price endpoint ─────────────────────────────────────────────────────────────

async def test_get_price_bitcoin(client: AsyncClient):
    mock_price = {
        "symbol": "bitcoin",
        "price_usd": 75000.0,
        "change_24h": 2.5,
        "market_cap": 1500000000000.0,
        "volume_24h": 50000000000.0,
    }

    with patch(
        "app.api.v1.endpoints.crypto.get_crypto_price",
        new_callable=AsyncMock,
        return_value=type("PriceBase", (), mock_price)(),
    ):
        response = await client.get("/api/v1/crypto/bitcoin/price")

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "bitcoin"
    assert data["price_usd"] == 75000.0
    assert data["change_24h"] == 2.5
    assert "id" in data
    assert "recorded_at" in data


async def test_get_price_invalid_symbol(client: AsyncClient):
    response = await client.get("/api/v1/crypto/dogecoin/price")
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]


async def test_get_price_ethereum(client: AsyncClient):
    mock_price = {
        "symbol": "ethereum",
        "price_usd": 3500.0,
        "change_24h": -1.2,
        "market_cap": 420000000000.0,
        "volume_24h": 15000000000.0,
    }

    with patch(
        "app.api.v1.endpoints.crypto.get_crypto_price",
        new_callable=AsyncMock,
        return_value=type("PriceBase", (), mock_price)(),
    ):
        response = await client.get("/api/v1/crypto/ethereum/price")

    assert response.status_code == 200
    assert response.json()["symbol"] == "ethereum"


# ── History endpoint ───────────────────────────────────────────────────────────

async def test_get_history_empty(client: AsyncClient):
    response = await client.get("/api/v1/crypto/bitcoin/history")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "bitcoin"
    assert data["prices"] == []
    assert data["total"] == 0


async def test_get_history_after_price_query(client: AsyncClient):
    mock_price = {
        "symbol": "bitcoin",
        "price_usd": 75000.0,
        "change_24h": 2.5,
        "market_cap": 1500000000000.0,
        "volume_24h": 50000000000.0,
    }

    with patch(
        "app.api.v1.endpoints.crypto.get_crypto_price",
        new_callable=AsyncMock,
        return_value=type("PriceBase", (), mock_price)(),
    ):
        await client.get("/api/v1/crypto/bitcoin/price")

    response = await client.get("/api/v1/crypto/bitcoin/history")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["prices"]) == 1
    assert data["prices"][0]["price_usd"] == 75000.0


async def test_get_history_invalid_symbol(client: AsyncClient):
    response = await client.get("/api/v1/crypto/dogecoin/history")
    assert response.status_code == 400


# ── Sentiment endpoint ─────────────────────────────────────────────────────────

async def test_get_sentiment_bitcoin(client: AsyncClient):
    mock_result = [
        {"label": "POSITIVE", "score": 0.99},
        {"label": "POSITIVE", "score": 0.98},
        {"label": "POSITIVE", "score": 0.97},
        {"label": "NEGATIVE", "score": 0.85},
        {"label": "POSITIVE", "score": 0.96},
    ]

    with patch(
        "app.services.sentiment_service.get_sentiment_pipeline"
    ) as mock_pipeline:
        mock_pipeline.return_value = lambda x: mock_result
        response = await client.get("/api/v1/crypto/bitcoin/sentiment")

    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "bitcoin"
    assert data["label"] == "POSITIVE"
    assert 0 <= data["score"] <= 1
    assert data["headlines_analyzed"] == 5


async def test_get_sentiment_invalid_symbol(client: AsyncClient):
    response = await client.get("/api/v1/crypto/dogecoin/sentiment")
    assert response.status_code == 400