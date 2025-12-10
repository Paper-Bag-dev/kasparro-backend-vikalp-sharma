from schemas.coinpaprika import CoinPaprikaItem
from schemas.csv_coin import CsvCoinItem
from schemas.normalized import NormalizedCoinModel
from schemas.coingecko import CoinGeckoItem


def normalize_coinpaprika(item: dict) -> NormalizedCoinModel:
    coin = CoinPaprikaItem(**item)

    usd = coin.quotes.get("USD", {}) if coin.quotes else {}

    return NormalizedCoinModel(
        source_name="coinpaprika",
        source_record_id=coin.id,
        symbol=coin.symbol,
        name=coin.name,
        price=usd.get("price"),
        market_cap=usd.get("market_cap"),
        volume_24h=usd.get("volume_24h"),
        ts=coin.last_updated,
        extra={k: v for k, v in item.items() if k not in {"id", "name", "symbol", "last_updated", "quotes"}}
    )

def normalize_csv_item(item: dict) -> NormalizedCoinModel:
    coin = CsvCoinItem(**item)

    return NormalizedCoinModel(
        source_name="csv",
        source_record_id=coin.id,
        symbol=coin.symbol,
        name=coin.name,
        price=coin.price,
        market_cap=coin.market_cap,
        volume_24h=coin.volume_24h,
        ts=coin.last_updated,
        extra={k: v for k, v in item.items()
               if k not in {"id", "name", "symbol", "price", "market_cap", "volume_24h", "last_updated"}}
    )

def normalize_coingecko(item: dict) -> NormalizedCoinModel:
    coin = CoinGeckoItem(**item)

    return NormalizedCoinModel(
        source_name="coingecko",
        source_record_id=coin.id,
        symbol=coin.symbol.upper() if coin.symbol else None,
        name=coin.name,
        price=coin.current_price,
        market_cap=coin.market_cap,
        volume_24h=coin.total_volume,
        ts=coin.last_updated,
        extra={
            k: v
            for k, v in item.items()
            if k
            not in {
                "id",
                "symbol",
                "name",
                "current_price",
                "market_cap",
                "total_volume",
                "last_updated",
            }
        },
    )
