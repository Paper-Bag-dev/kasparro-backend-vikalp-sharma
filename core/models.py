from sqlalchemy import Column, Integer, String, DateTime, Float, UniqueConstraint, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .db import Base

class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"
    id = Column(Integer, primary_key=True)
    source_record_id = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())


class RawCsvCoin(Base):
    __tablename__ = "raw_csv_coins"
    id = Column(Integer, primary_key=True)
    source_record_id = Column(String, index=True)
    payload = Column(JSONB, nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class RawCoinGecko(Base):
    __tablename__ = "raw_coingecko"

    id = Column(Integer, primary_key=True, index=True)
    source_record_id = Column(String, index=True)
    payload = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class NormalizedCoins(Base):
    __tablename__ = "normalized_coins"
    id = Column(Integer, primary_key=True)
    source_name = Column(String, index=True)
    source_record_id = Column(String, index=True)
    symbol = Column(String)
    name = Column(String)
    price = Column(Float)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    ts = Column(DateTime(timezone=True))
    extra = Column(JSONB)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("source_record_id", "ts", name="uix_source_record_ts"),
    )



class ETLRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    status = Column(String, nullable=False)
    records_processed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
