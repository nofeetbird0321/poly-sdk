"""Basic usage example for Polymarket SDK.

This example demonstrates:
- Price utilities and validation
- Arbitrage detection
- Effective price calculation
"""

import asyncio
from polymarket_sdk import (
    round_price,
    validate_price,
    calculate_buy_amount,
    get_effective_prices,
    check_arbitrage,
    format_usdc,
    calculate_pnl,
)


def demonstrate_price_utilities():
    """Demonstrate price utility functions."""
    print("=" * 60)
    print("Price Utilities Demo")
    print("=" * 60)

    # Round prices to different tick sizes
    price = 0.523
    print(f"\nOriginal price: {price}")
    print(f"Rounded (floor, 0.01): {round_price(price, '0.01', 'floor')}")
    print(f"Rounded (ceil, 0.01): {round_price(price, '0.01', 'ceil')}")
    print(f"Rounded (round, 0.01): {round_price(price, '0.01', 'round')}")

    # Validate price
    valid, error = validate_price(0.525, "0.01")
    print(f"\nValidate 0.525 with tick 0.01: valid={valid}")
    if error:
        print(f"Error: {error}")

    # Calculate order amounts
    shares = 100
    price = 0.52
    amount = calculate_buy_amount(price, shares)
    print(f"\nBuy {shares} shares @ {price}: {format_usdc(amount)}")


def demonstrate_effective_prices():
    """Demonstrate effective price calculation for Polymarket."""
    print("\n" + "=" * 60)
    print("Effective Prices Demo (Considering Mirror Orders)")
    print("=" * 60)

    # Example orderbook prices
    yes_ask = 0.48
    yes_bid = 0.46
    no_ask = 0.54
    no_bid = 0.52

    print(f"\nOrderbook prices:")
    print(f"YES: bid={yes_bid}, ask={yes_ask}")
    print(f"NO: bid={no_bid}, ask={no_ask}")

    # Calculate effective prices
    effective = get_effective_prices(yes_ask, yes_bid, no_ask, no_bid)
    print(f"\nEffective prices (considering mirror orders):")
    print(f"Buy YES: {effective['effective_buy_yes']:.4f}")
    print(f"Buy NO: {effective['effective_buy_no']:.4f}")
    print(f"Sell YES: {effective['effective_sell_yes']:.4f}")
    print(f"Sell NO: {effective['effective_sell_no']:.4f}")

    # Calculate costs
    long_cost = effective["effective_buy_yes"] + effective["effective_buy_no"]
    short_revenue = effective["effective_sell_yes"] + effective["effective_sell_no"]
    print(f"\nLong cost (buy both): {format_usdc(long_cost)}")
    print(f"Short revenue (sell both): {format_usdc(short_revenue)}")


def demonstrate_arbitrage_detection():
    """Demonstrate arbitrage detection."""
    print("\n" + "=" * 60)
    print("Arbitrage Detection Demo")
    print("=" * 60)

    # Example 1: Long arbitrage opportunity
    yes_ask = 0.48
    no_ask = 0.50
    yes_bid = 0.46
    no_bid = 0.48

    print(f"\nExample 1: Long arb opportunity")
    print(f"YES: ask={yes_ask}, bid={yes_bid}")
    print(f"NO: ask={no_ask}, bid={no_bid}")

    arb = check_arbitrage(yes_ask, no_ask, yes_bid, no_bid)
    if arb:
        print(f"\n✅ {arb['type'].upper()} ARBITRAGE FOUND!")
        print(f"Profit: {format_usdc(arb['profit'])} ({arb['profit']*100:.2f}%)")
        print(f"Strategy: {arb['description']}")
    else:
        print("\n❌ No arbitrage opportunity")

    # Example 2: No arbitrage
    yes_ask = 0.52
    no_ask = 0.50
    yes_bid = 0.50
    no_bid = 0.48

    print(f"\nExample 2: No arbitrage")
    print(f"YES: ask={yes_ask}, bid={yes_bid}")
    print(f"NO: ask={no_ask}, bid={no_bid}")

    arb = check_arbitrage(yes_ask, no_ask, yes_bid, no_bid)
    if arb:
        print(f"\n✅ {arb['type'].upper()} ARBITRAGE FOUND!")
        print(f"Profit: {format_usdc(arb['profit'])} ({arb['profit']*100:.2f}%)")
        print(f"Strategy: {arb['description']}")
    else:
        print("\n❌ No arbitrage opportunity")


def demonstrate_pnl_calculation():
    """Demonstrate PnL calculation."""
    print("\n" + "=" * 60)
    print("PnL Calculation Demo")
    print("=" * 60)

    entry_price = 0.40
    current_price = 0.55
    size = 100

    pnl_data = calculate_pnl(entry_price, current_price, size, "long")
    print(f"\nLong position:")
    print(f"Entry: {format_usdc(entry_price)}, Current: {format_usdc(current_price)}")
    print(f"Size: {size} shares")
    print(f"PnL: {format_usdc(pnl_data['pnl'])} ({pnl_data['pnl_percent']:.1f}%)")


def main():
    """Run all demonstrations."""
    demonstrate_price_utilities()
    demonstrate_effective_prices()
    demonstrate_arbitrage_detection()
    demonstrate_pnl_calculation()
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
