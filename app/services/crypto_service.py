import aiohttp
from app.schemas.price import PriceBase

COINGECKO_URL = "https://api.coingecko.com/api/v3"

SUPPORTED_SYMBOLS = {
    "bitcoin": "bitcoin",
    "ethereum": "ethereum",
    "litecoin": "litecoin",
    "btc": "bitcoin",
    "eth": "ethereum",
    "ltc": "litecoin",
}


async def get_crypto_price(symbol: str) -> PriceBase:
    coin_id = SUPPORTED_SYMBOLS.get(symbol.lower())
    if not coin_id:
        raise ValueError(f"Symbol '{symbol}' not supported. Use: bitcoin, ethereum, litecoin")

    url = f"{COINGECKO_URL}/coins/{coin_id}"
    params = {"localization": "false", "tickers": "false", "community_data": "false"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise ConnectionError(f"CoinGecko API error: {response.status}")
            data = await response.json()

    market_data = data.get("market_data", {})

    return PriceBase(
        symbol=coin_id,
        price_usd=market_data["current_price"]["usd"],
        change_24h=market_data.get("price_change_percentage_24h"),
        market_cap=market_data.get("market_cap", {}).get("usd"),
        volume_24h=market_data.get("total_volume", {}).get("usd"),
    )