"""Price utilities for Polymarket trading.

This module provides helper functions for:
- Price validation and rounding to tick size
- Size validation
- Order amount calculation
- Arbitrage detection considering Polymarket's mirror orderbook
"""

from typing import Dict, Literal, Optional, Tuple
import math


# Tick size types as defined by Polymarket
TickSize = Literal["0.1", "0.01", "0.001", "0.0001"]


# Rounding configuration for each tick size
ROUNDING_CONFIG: Dict[TickSize, Dict[str, int]] = {
    "0.1": {"price": 1, "size": 2, "amount": 2},
    "0.01": {"price": 2, "size": 2, "amount": 4},
    "0.001": {"price": 3, "size": 2, "amount": 5},
    "0.0001": {"price": 4, "size": 2, "amount": 6},
}


def round_price(
    price: float,
    tick_size: TickSize,
    direction: Literal["floor", "ceil", "round"] = "round",
) -> float:
    """Round a price to the appropriate tick size.

    Args:
        price: The price to round (0 to 1).
        tick_size: The tick size for the market.
        direction: Rounding direction - 'floor' for sells, 'ceil' for buys,
            'round' for midpoint.

    Returns:
        Rounded price clamped to valid range [0.001, 0.999].

    Examples:
        >>> round_price(0.523, "0.01", "floor")
        0.52
        >>> round_price(0.523, "0.01", "ceil")
        0.53
    """
    decimals = ROUNDING_CONFIG[tick_size]["price"]
    multiplier = 10 ** decimals

    if direction == "floor":
        rounded = math.floor(price * multiplier) / multiplier
    elif direction == "ceil":
        rounded = math.ceil(price * multiplier) / multiplier
    else:
        rounded = round(price * multiplier) / multiplier

    # Clamp to valid price range
    return max(0.001, min(0.999, rounded))


def round_size(size: float) -> float:
    """Round a size to valid decimals (always 2 decimal places).

    Args:
        size: The size to round.

    Returns:
        Rounded size with 2 decimal places.
    """
    return round(size * 100) / 100


def validate_price(price: float, tick_size: TickSize) -> Tuple[bool, Optional[str]]:
    """Validate a price is within valid range and tick size.

    Args:
        price: The price to validate.
        tick_size: The tick size for the market.

    Returns:
        Tuple of (is_valid, error_message).
    """
    # Check range
    if price < 0.001 or price > 0.999:
        return False, "Price must be between 0.001 and 0.999"

    # Check tick size alignment
    decimals = ROUNDING_CONFIG[tick_size]["price"]
    multiplier = 10 ** decimals
    rounded = round(price * multiplier) / multiplier

    if abs(price - rounded) > 1e-10:
        return (
            False,
            f"Price {price} does not align with tick size {tick_size}. "
            f"Use {rounded} instead.",
        )

    return True, None


def validate_size(size: float, min_order_size: float = 0.1) -> Tuple[bool, Optional[str]]:
    """Validate minimum size requirements.

    Args:
        size: The size to validate.
        min_order_size: Minimum order size from market config (usually 0.1).

    Returns:
        Tuple of (is_valid, error_message).
    """
    if size < min_order_size:
        return (
            False,
            f"Size {size} is below minimum order size {min_order_size}",
        )

    return True, None


def calculate_buy_amount(price: float, size: float) -> float:
    """Calculate the amount needed for a buy order (in USDC).

    Args:
        price: Price per share.
        size: Number of shares to buy.

    Returns:
        Amount in USDC.
    """
    return price * size


def calculate_sell_payout(price: float, size: float) -> float:
    """Calculate the payout for a sell order (in USDC).

    Args:
        price: Price per share.
        size: Number of shares to sell.

    Returns:
        Amount in USDC.
    """
    return price * size


def calculate_shares_for_amount(amount: float, price: float) -> float:
    """Calculate number of shares that can be bought with a given amount.

    Args:
        amount: USDC amount to spend.
        price: Price per share.

    Returns:
        Number of shares (rounded to 2 decimals).
    """
    return round_size(amount / price)


def calculate_spread(bid: float, ask: float) -> float:
    """Calculate the spread between bid and ask.

    Args:
        bid: Highest bid price.
        ask: Lowest ask price.

    Returns:
        Spread as a decimal (0 to 1).
    """
    return ask - bid


def calculate_midpoint(bid: float, ask: float) -> float:
    """Calculate the midpoint price between bid and ask.

    Args:
        bid: Highest bid price.
        ask: Lowest ask price.

    Returns:
        Midpoint price.
    """
    return (bid + ask) / 2


def get_effective_prices(
    yes_ask: float,
    yes_bid: float,
    no_ask: float,
    no_bid: float,
) -> Dict[str, float]:
    """Calculate effective prices considering Polymarket's mirror orderbook.

    Polymarket key feature: Buy YES @ P = Sell NO @ (1-P)
    The same order appears in both orderbooks.

    Args:
        yes_ask: YES token lowest ask price.
        yes_bid: YES token highest bid price.
        no_ask: NO token lowest ask price.
        no_bid: NO token highest bid price.

    Returns:
        Dict with effective prices for buying and selling YES and NO.
    """
    return {
        # Buy YES: direct buy YES.ask or via selling NO (cost = 1 - NO.bid)
        "effective_buy_yes": min(yes_ask, 1 - no_bid),
        # Buy NO: direct buy NO.ask or via selling YES (cost = 1 - YES.bid)
        "effective_buy_no": min(no_ask, 1 - yes_bid),
        # Sell YES: direct sell YES.bid or via buying NO (revenue = 1 - NO.ask)
        "effective_sell_yes": max(yes_bid, 1 - no_ask),
        # Sell NO: direct sell NO.bid or via buying YES (revenue = 1 - YES.ask)
        "effective_sell_no": max(no_bid, 1 - yes_ask),
    }


def check_arbitrage(
    yes_ask: float,
    no_ask: float,
    yes_bid: float,
    no_bid: float,
) -> Optional[Dict[str, any]]:
    """Check if there's an arbitrage opportunity using effective prices.

    Long arb: Buy YES + Buy NO < 1 (using effective buy prices)
    Short arb: Sell YES + Sell NO > 1 (using effective sell prices)

    Args:
        yes_ask: Lowest ask for YES token.
        no_ask: Lowest ask for NO token.
        yes_bid: Highest bid for YES token.
        no_bid: Highest bid for NO token.

    Returns:
        Dict with arbitrage info or None if no opportunity.
    """
    # Calculate effective prices
    effective = get_effective_prices(yes_ask, yes_bid, no_ask, no_bid)

    # Long arbitrage: Buy complete set (YES + NO) cheaper than $1
    effective_long_cost = (
        effective["effective_buy_yes"] + effective["effective_buy_no"]
    )
    long_profit = 1 - effective_long_cost

    if long_profit > 0:
        return {
            "type": "long",
            "profit": long_profit,
            "description": (
                f"Buy YES @ {effective['effective_buy_yes']:.4f} + "
                f"NO @ {effective['effective_buy_no']:.4f}, Merge for $1"
            ),
        }

    # Short arbitrage: Sell complete set (YES + NO) for more than $1
    effective_short_revenue = (
        effective["effective_sell_yes"] + effective["effective_sell_no"]
    )
    short_profit = effective_short_revenue - 1

    if short_profit > 0:
        return {
            "type": "short",
            "profit": short_profit,
            "description": (
                f"Split $1, Sell YES @ {effective['effective_sell_yes']:.4f} + "
                f"NO @ {effective['effective_sell_no']:.4f}"
            ),
        }

    return None


def format_price(price: float, tick_size: Optional[TickSize] = None) -> str:
    """Format price for display.

    Args:
        price: Price to format.
        tick_size: Optional tick size for precision.

    Returns:
        Formatted price string.
    """
    decimals = ROUNDING_CONFIG[tick_size]["price"] if tick_size else 4
    return f"{price:.{decimals}f}"


def format_usdc(amount: float) -> str:
    """Format amount in USDC.

    Args:
        amount: Amount to format.

    Returns:
        Formatted USDC string.
    """
    return f"${amount:.2f}"


def calculate_pnl(
    entry_price: float,
    current_price: float,
    size: float,
    side: Literal["long", "short"] = "long",
) -> Dict[str, float]:
    """Calculate PnL for a position.

    Args:
        entry_price: Average entry price.
        current_price: Current market price.
        size: Position size.
        side: 'long' for YES, 'short' for NO.

    Returns:
        Dict with 'pnl' (absolute) and 'pnl_percent' (percentage).
    """
    if side == "long":
        pnl = (current_price - entry_price) * size
        pnl_percent = ((current_price - entry_price) / entry_price) * 100
    else:
        pnl = (entry_price - current_price) * size
        pnl_percent = ((entry_price - current_price) / entry_price) * 100

    return {"pnl": pnl, "pnl_percent": pnl_percent}
