"""Initialize core package."""

from polymarket_sdk.core.errors import (
    ErrorCode,
    PolymarketError,
    with_retry,
)
from polymarket_sdk.core.types import (
    KLineInterval,
    KLineCandle,
    SpreadDataPoint,
    EffectivePrices,
    RealtimeSpreadAnalysis,
    OrderbookSide,
    OrderbookSummary,
    ProcessedOrderbook,
    ArbitrageOpportunity,
    PriceUpdate,
    BookLevel,
    BookUpdate,
    TokenInfo,
    MarketTokens,
    UnifiedMarket,
    DualKLineData,
    get_interval_ms,
)

__all__ = [
    # Errors
    "ErrorCode",
    "PolymarketError",
    "with_retry",
    # Types
    "KLineInterval",
    "KLineCandle",
    "SpreadDataPoint",
    "EffectivePrices",
    "RealtimeSpreadAnalysis",
    "OrderbookSide",
    "OrderbookSummary",
    "ProcessedOrderbook",
    "ArbitrageOpportunity",
    "PriceUpdate",
    "BookLevel",
    "BookUpdate",
    "TokenInfo",
    "MarketTokens",
    "UnifiedMarket",
    "DualKLineData",
    "get_interval_ms",
]
