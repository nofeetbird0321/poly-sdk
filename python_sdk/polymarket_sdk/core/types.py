"""Common types used across the Polymarket SDK.

This module defines data classes and types following Google Python style guide,
using dataclasses and type hints for clarity and type safety.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional, Union


# K-Line interval types
KLineInterval = Literal["30s", "1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d"]


@dataclass
class KLineCandle:
    """K-Line candle data for market analysis.

    Attributes:
        timestamp: Unix timestamp in milliseconds.
        open: Opening price.
        high: Highest price.
        low: Lowest price.
        close: Closing price.
        volume: Trading volume.
        trade_count: Number of trades.
        buy_volume: Volume from buy orders.
        sell_volume: Volume from sell orders.
    """

    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: int
    buy_volume: float
    sell_volume: float


@dataclass
class SpreadDataPoint:
    """Historical spread analysis based on trade close prices.

    Used for historical trend analysis and backtesting.
    Note: arbOpportunity is a reference signal only, not actual tradeable arbitrage.

    Attributes:
        timestamp: Unix timestamp in milliseconds.
        yes_price: YES token close price from trades.
        no_price: NO token close price from trades.
        price_sum: YES + NO close price sum.
        price_spread: price_sum - 1 (deviation from equilibrium).
        arb_opportunity: Reference signal based on price deviation.
    """

    timestamp: int
    yes_price: float
    no_price: float
    price_sum: float
    price_spread: float
    arb_opportunity: Literal["LONG", "SHORT", ""]


@dataclass
class EffectivePrices:
    """Effective prices considering Polymarket orderbook mirror property.

    Polymarket key feature: Buy YES @ P = Sell NO @ (1-P)
    The same order appears in both orderbooks.

    Attributes:
        effective_buy_yes: Lowest cost to buy YES.
        effective_buy_no: Lowest cost to buy NO.
        effective_sell_yes: Highest revenue from selling YES.
        effective_sell_no: Highest revenue from selling NO.
    """

    effective_buy_yes: float
    effective_buy_no: float
    effective_sell_yes: float
    effective_sell_no: float


@dataclass
class RealtimeSpreadAnalysis:
    """Real-time spread analysis based on orderbook bid/ask.

    Used for live trading and arbitrage execution.
    Note: Cannot build historical curve - Polymarket doesn't save orderbook history.

    Attributes:
        timestamp: Unix timestamp in milliseconds.
        yes_bid: YES token best bid price.
        yes_ask: YES token best ask price.
        no_bid: NO token best bid price.
        no_ask: NO token best ask price.
        ask_sum: YES_ask + NO_ask (buy both sides cost).
        bid_sum: YES_bid + NO_bid (sell both sides revenue).
        ask_spread: ask_sum - 1 (negative = long arb space).
        bid_spread: bid_sum - 1 (positive = short arb space).
        long_arb_profit: 1 - ask_sum, > 0 indicates long arb opportunity.
        short_arb_profit: bid_sum - 1, > 0 indicates short arb opportunity.
        arb_opportunity: Current arbitrage direction.
        arb_profit_percent: Arbitrage profit percentage.
    """

    timestamp: int
    yes_bid: float
    yes_ask: float
    no_bid: float
    no_ask: float
    ask_sum: float
    bid_sum: float
    ask_spread: float
    bid_spread: float
    long_arb_profit: float
    short_arb_profit: float
    arb_opportunity: Literal["LONG", "SHORT", ""]
    arb_profit_percent: float


@dataclass
class OrderbookSide:
    """Orderbook data for one side (YES or NO token).

    Attributes:
        bid: Best bid price.
        ask: Best ask price.
        bid_size: Size at best bid.
        ask_size: Size at best ask.
        bid_depth: Total bid depth.
        ask_depth: Total ask depth.
        spread: ask - bid.
        token_id: Optional token identifier.
    """

    bid: float
    ask: float
    bid_size: float
    ask_size: float
    bid_depth: float
    ask_depth: float
    spread: float
    token_id: Optional[str] = None


@dataclass
class OrderbookSummary:
    """Summary of processed orderbook with arbitrage analysis.

    Attributes:
        ask_sum: Raw ask sum (may include duplicates).
        bid_sum: Raw bid sum (may include duplicates).
        effective_prices: Effective prices considering mirror orders.
        effective_long_cost: effective_buy_yes + effective_buy_no.
        effective_short_revenue: effective_sell_yes + effective_sell_no.
        long_arb_profit: 1 - effective_long_cost.
        short_arb_profit: effective_short_revenue - 1.
        total_bid_depth: Combined bid depth.
        total_ask_depth: Combined ask depth.
        imbalance_ratio: Depth imbalance ratio.
        yes_spread: YES token spread.
    """

    ask_sum: float
    bid_sum: float
    effective_prices: EffectivePrices
    effective_long_cost: float
    effective_short_revenue: float
    long_arb_profit: float
    short_arb_profit: float
    total_bid_depth: float
    total_ask_depth: float
    imbalance_ratio: float
    yes_spread: float


@dataclass
class ProcessedOrderbook:
    """Processed orderbook with complete analysis.

    Attributes:
        yes: YES token orderbook side.
        no: NO token orderbook side.
        summary: Aggregated summary and arbitrage analysis.
    """

    yes: OrderbookSide
    no: OrderbookSide
    summary: OrderbookSummary


@dataclass
class ArbitrageOpportunity:
    """Arbitrage opportunity details.

    Attributes:
        type: Type of arbitrage ('long' or 'short').
        profit: Profit amount.
        action: Description of action to take.
        expected_profit: Expected profit amount.
    """

    type: Literal["long", "short"]
    profit: float
    action: str
    expected_profit: float


@dataclass
class PriceUpdate:
    """Price update from WebSocket.

    Attributes:
        asset_id: Asset identifier.
        price: Current price.
        midpoint: Midpoint between bid and ask.
        spread: Bid-ask spread.
        timestamp: Update timestamp.
    """

    asset_id: str
    price: float
    midpoint: float
    spread: float
    timestamp: int


@dataclass
class BookLevel:
    """Single orderbook level.

    Attributes:
        price: Price level.
        size: Size at this level.
    """

    price: float
    size: float


@dataclass
class BookUpdate:
    """Orderbook update from WebSocket.

    Attributes:
        asset_id: Asset identifier.
        bids: List of bid levels.
        asks: List of ask levels.
        timestamp: Update timestamp.
    """

    asset_id: str
    bids: List[BookLevel]
    asks: List[BookLevel]
    timestamp: int


@dataclass
class TokenInfo:
    """Token information within a market.

    Attributes:
        token_id: Token identifier.
        price: Current price.
    """

    token_id: str
    price: float


@dataclass
class MarketTokens:
    """Token pair for a market.

    Attributes:
        yes: YES token information.
        no: NO token information.
    """

    yes: TokenInfo
    no: TokenInfo


@dataclass
class UnifiedMarket:
    """Unified market type merged from Gamma and CLOB APIs.

    Attributes:
        condition_id: Unique condition identifier.
        slug: Market slug for URL.
        question: Market question.
        description: Optional market description.
        tokens: YES and NO token information.
        volume: Total volume.
        volume_24hr: 24-hour volume.
        liquidity: Market liquidity.
        spread: Bid-ask spread.
        one_day_price_change: 1-day price change.
        one_week_price_change: 1-week price change.
        active: Whether market is active.
        closed: Whether market is closed.
        accepting_orders: Whether market accepts new orders.
        end_date: Market end date.
        source: Data source.
    """

    condition_id: str
    slug: str
    question: str
    tokens: MarketTokens
    volume: float
    liquidity: float
    active: bool
    closed: bool
    accepting_orders: bool
    end_date: datetime
    source: Literal["gamma", "clob", "merged"]
    description: Optional[str] = None
    volume_24hr: Optional[float] = None
    spread: Optional[float] = None
    one_day_price_change: Optional[float] = None
    one_week_price_change: Optional[float] = None


@dataclass
class DualKLineData:
    """Dual K-line data for YES and NO tokens.

    Attributes:
        condition_id: Market condition ID.
        interval: K-line interval.
        yes: YES token candles.
        no: NO token candles.
        market: Optional market information.
        spread_analysis: Historical spread analysis.
        realtime_spread: Real-time spread snapshot.
        current_orderbook: Current orderbook data.
    """

    condition_id: str
    interval: KLineInterval
    yes: List[KLineCandle]
    no: List[KLineCandle]
    market: Optional[UnifiedMarket] = None
    spread_analysis: Optional[List[SpreadDataPoint]] = None
    realtime_spread: Optional[RealtimeSpreadAnalysis] = None
    current_orderbook: Optional[ProcessedOrderbook] = None


# Time conversion constants
_MILLISECONDS_PER_SECOND = 1000
_SECONDS_PER_MINUTE = 60
_MINUTES_PER_HOUR = 60
_HOURS_PER_DAY = 24


def get_interval_ms(interval: KLineInterval) -> int:
    """Convert interval to milliseconds.

    Args:
        interval: K-line interval.

    Returns:
        Interval duration in milliseconds.
    """
    interval_map: Dict[KLineInterval, int] = {
        "30s": 30 * _MILLISECONDS_PER_SECOND,
        "1m": _SECONDS_PER_MINUTE * _MILLISECONDS_PER_SECOND,
        "5m": 5 * _SECONDS_PER_MINUTE * _MILLISECONDS_PER_SECOND,
        "15m": 15 * _SECONDS_PER_MINUTE * _MILLISECONDS_PER_SECOND,
        "30m": 30 * _SECONDS_PER_MINUTE * _MILLISECONDS_PER_SECOND,
        "1h": _SECONDS_PER_MINUTE * _MINUTES_PER_HOUR * _MILLISECONDS_PER_SECOND,
        "4h": 4 * _SECONDS_PER_MINUTE * _MINUTES_PER_HOUR * _MILLISECONDS_PER_SECOND,
        "12h": 12 * _SECONDS_PER_MINUTE * _MINUTES_PER_HOUR * _MILLISECONDS_PER_SECOND,
        "1d": _HOURS_PER_DAY * _SECONDS_PER_MINUTE * _MINUTES_PER_HOUR * _MILLISECONDS_PER_SECOND,
    }
    return interval_map[interval]
