# Polymarket Python SDK

Python SDK for Polymarket - prediction markets trading, smart money analysis, and market data.

**Note**: This is a Python port of the TypeScript SDK with the same functionality.

## Installation

```bash
pip install polymarket-sdk
```

## Quick Start

```python
from polymarket_sdk import PolymarketSDK

# Initialize SDK
sdk = PolymarketSDK()

# Get market by slug or condition ID
market = await sdk.get_market('will-trump-win-2024')
print(f"YES price: {market.tokens.yes.price}")

# Get processed orderbook with analytics
orderbook = await sdk.get_orderbook(market.condition_id)
print(f"Long arb profit: {orderbook.summary.long_arb_profit}")

# Detect arbitrage
arb = await sdk.detect_arbitrage(market.condition_id)
if arb:
    print(f"{arb.type} arb: {arb.profit * 100}% profit")
```

## Features

- **Data API Client**: Positions, trades, leaderboard
- **Gamma API Client**: Markets, events, trending
- **CLOB API Client**: Orderbook, trading
- **WebSocket**: Real-time price updates
- **Trading Client**: Order execution (GTC, GTD, FOK, FAK)
- **CTF Client**: On-chain operations (split, merge, redeem)
- **Wallet Service**: Smart money analysis
- **Market Service**: K-lines and signals
- **Arbitrage Service**: Real-time arbitrage detection
- **Price Utilities**: Validation, rounding, calculations

## Documentation

See the TypeScript SDK documentation for detailed API reference.

## Requirements

- Python 3.8+
- aiohttp
- web3
- eth-account

## License

MIT
