from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.price import Price
from app.schemas.price import PriceBase

class PriceRepository:

    async def save_price(
        self, db: AsyncSession, price_data: PriceBase, symbol: str
    ) -> Price:
        price = Price(
            symbol=symbol.lower(),
            price_usd=price_data.price_usd,
            change_24h=price_data.change_24h,
            market_cap=price_data.market_cap,
            volume_24h=price_data.volume_24h,
        )
        db.add(price)
        await db.flush()
        await db.refresh(price)
        return price

    async def get_latest_price(
        self, db: AsyncSession, symbol: str
    ) -> Price | None:
        stmt = (
            select(Price)
            .where(Price.symbol == symbol.lower())
            .order_by(desc(Price.recorded_at))
            .limit(1)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_price_history(
        self, db: AsyncSession, symbol: str, limit: int = 50
    ) -> list[Price]:
        stmt = (
            select(Price)
            .where(Price.symbol == symbol.lower())
            .order_by(desc(Price.recorded_at))
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_total_records(
        self, db: AsyncSession, symbol: str
    ) -> int:
        stmt = (
            select(Price)
            .where(Price.symbol == symbol.lower())
        )
        result = await db.execute(stmt)
        return len(result.scalars().all())


price_repository = PriceRepository()