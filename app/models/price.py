from datetime import datetime
from sqlalchemy import String, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    price_usd: Mapped[float] = mapped_column(Float, nullable=False)
    change_24h: Mapped[float] = mapped_column(Float, nullable=True)
    market_cap: Mapped[float] = mapped_column(Float, nullable=True)
    volume_24h: Mapped[float] = mapped_column(Float, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    def __repr__(self) -> str:
        return f"Price(id={self.id}, symbol={self.symbol}, price_usd={self.price_usd})"