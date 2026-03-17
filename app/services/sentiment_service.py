from transformers import pipeline
from app.schemas.price import SentimentResponse

CRYPTO_HEADLINES = {
    "bitcoin": [
        "Bitcoin reaches new all-time high amid institutional adoption",
        "Bitcoin network hash rate hits record levels",
        "Major bank announces Bitcoin custody services",
        "Bitcoin ETF sees record inflows this week",
        "Bitcoin volatility increases as market uncertainty grows",
    ],
    "ethereum": [
        "Ethereum network upgrades improve transaction speeds",
        "Ethereum DeFi ecosystem continues rapid expansion",
        "Major protocol launches on Ethereum mainnet",
        "Ethereum staking rewards attract institutional investors",
        "Ethereum gas fees rise amid network congestion",
    ],
    "litecoin": [
        "Litecoin adoption grows among payment processors",
        "Litecoin network completes successful upgrade",
        "Litecoin transaction volume reaches yearly high",
        "Litecoin halving approaches as miners prepare",
        "Litecoin price correlates with broader crypto market",
    ],
}

_sentiment_pipeline = None


def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )
    return _sentiment_pipeline


async def analyze_sentiment(symbol: str) -> SentimentResponse:
    coin_id = symbol.lower()
    headlines = CRYPTO_HEADLINES.get(coin_id)
    if not headlines:
        raise ValueError(f"Symbol '{symbol}' not supported for sentiment analysis")

    sentiment_pipeline = get_sentiment_pipeline()
    results = sentiment_pipeline(headlines)

    positive_scores = [
        r["score"] for r in results if r["label"] == "POSITIVE"
    ]
    negative_scores = [
        r["score"] for r in results if r["label"] == "NEGATIVE"
    ]

    if len(positive_scores) >= len(negative_scores):
        label = "POSITIVE"
        score = sum(positive_scores) / len(positive_scores) if positive_scores else 0.0
    else:
        label = "NEGATIVE"
        score = sum(negative_scores) / len(negative_scores) if negative_scores else 0.0

    return SentimentResponse(
        symbol=coin_id,
        label=label,
        score=round(score, 4),
        headlines_analyzed=len(headlines),
    )