"""Polymarket SDK - Python implementation.

A comprehensive SDK for interacting with Polymarket prediction markets,
including trading, market data, and smart money analysis.

This module follows Google Python Style Guide conventions.
"""

__version__ = "0.2.1"

from polymarket_sdk.core import (
    ErrorCode,
    PolymarketError,
    with_retry,
    KLineInterval,
    KLineCandle,
    ProcessedOrderbook,
    ArbitrageOpportunity,
    UnifiedMarket,
)
from polymarket_sdk.utils import (
    TickSize,
    round_price,
    validate_price,
    calculate_buy_amount,
    get_effective_prices,
    check_arbitrage,
    format_usdc,
    calculate_pnl,
)

__all__ = [
    # Version
    "__version__",
    # Core errors
    "ErrorCode",
    "PolymarketError",
    "with_retry",
    # Core types
    "KLineInterval",
    "KLineCandle",
    "ProcessedOrderbook",
    "ArbitrageOpportunity",
    "UnifiedMarket",
    # Price utils
    "TickSize",
    "round_price",
    "validate_price",
    "calculate_buy_amount",
    "get_effective_prices",
    "check_arbitrage",
    "format_usdc",
    "calculate_pnl",
]
