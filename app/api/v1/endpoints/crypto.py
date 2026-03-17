from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.price import PriceResponse, PriceHistoryResponse, SentimentResponse
from app.services.crypto_service import get_crypto_price
from app.services.sentiment_service import analyze_sentiment
from app.repositories.price_repository import price_repository

router = APIRouter()

SUPPORTED_SYMBOLS = ["bitcoin", "ethereum", "litecoin", "btc", "eth", "ltc"]


@router.get("/{symbol}/price", response_model=PriceResponse)
async def get_price(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    if symbol.lower() not in SUPPORTED_SYMBOLS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol '{symbol}' not supported. Use: bitcoin, ethereum, litecoin",
        )

    try:
        price_data = await get_crypto_price(symbol)
        saved_price = await price_repository.save_price(db, price_data, symbol)
        return saved_price
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )


@router.get("/{symbol}/history", response_model=PriceHistoryResponse)
async def get_history(
    symbol: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    if symbol.lower() not in SUPPORTED_SYMBOLS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol '{symbol}' not supported. Use: bitcoin, ethereum, litecoin",
        )

    prices = await price_repository.get_price_history(db, symbol, limit)
    total = await price_repository.get_total_records(db, symbol)

    return PriceHistoryResponse(
        symbol=symbol.lower(),
        prices=prices,
        total=total,
    )


@router.get("/{symbol}/sentiment", response_model=SentimentResponse)
async def get_sentiment(symbol: str):
    if symbol.lower() not in SUPPORTED_SYMBOLS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol '{symbol}' not supported. Use: bitcoin, ethereum, litecoin",
        )

    try:
        return await analyze_sentiment(symbol)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )