# Python SDK Development Guide

## Overview

This Python SDK is a port of the TypeScript Polymarket SDK, following Google's Python Style Guide.

## Project Structure

```
python_sdk/
├── polymarket_sdk/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── errors.py        # Error handling
│   │   └── types.py         # Type definitions
│   ├── clients/             # API clients (to be implemented)
│   │   ├── __init__.py
│   │   ├── data_api.py      # Data API client
│   │   ├── gamma_api.py     # Gamma API client
│   │   ├── clob_api.py      # CLOB API client
│   │   ├── trading_client.py # Trading client
│   │   └── ctf_client.py    # CTF client
│   ├── services/            # High-level services (to be implemented)
│   │   ├── __init__.py
│   │   ├── wallet_service.py
│   │   ├── market_service.py
│   │   └── arbitrage_service.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── price_utils.py   # Price utilities ✅
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_errors.py       # ✅
│   └── test_price_utils.py  # ✅
├── examples/                # Example scripts
│   └── 01_basic_usage.py    # ✅
├── pyproject.toml           # Project configuration ✅
├── setup.py                 # Setup script ✅
├── .pylintrc                # Linting configuration ✅
├── .gitignore               # Git ignore rules ✅
├── .env.example             # Environment variables template ✅
├── README.md                # Main documentation ✅
├── SECURITY_ANALYSIS.md     # Security analysis ✅
└── DEVELOPMENT.md           # This file ✅
```

## Development Status

### ✅ Completed

1. **Project Setup**
   - pyproject.toml with dependencies
   - setup.py for package installation
   - .pylintrc for code quality
   - .gitignore for version control
   - .env.example for configuration

2. **Core Module**
   - Error handling (errors.py)
   - Type definitions (types.py)
   - Following Google Python Style Guide
   - Comprehensive docstrings

3. **Utils Module**
   - Price utilities (price_utils.py)
   - Arbitrage detection
   - Effective price calculation
   - Input validation

4. **Tests**
   - Unit tests for errors module
   - Unit tests for price utilities
   - Using pytest framework

5. **Documentation**
   - Security analysis report
   - Example usage script
   - Development guide

### 🔄 To Be Implemented

1. **API Clients**
   - DataApiClient - Positions, trades, leaderboard
   - GammaApiClient - Markets, events
   - ClobApiClient - Orderbook, trading
   - TradingClient - Order execution
   - CTFClient - On-chain operations
   - WebSocketManager - Real-time updates
   - BridgeClient - Cross-chain deposits
   - SwapService - DEX swaps

2. **Services**
   - WalletService - Smart money analysis
   - MarketService - K-lines and signals
   - RealtimeService - WebSocket subscriptions
   - ArbitrageService - Real-time arbitrage
   - AuthorizationService - Trading approvals

3. **Integration Tests**
   - API client tests
   - Service tests
   - End-to-end tests

## Setup for Development

### 1. Create Virtual Environment

```bash
cd python_sdk
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your credentials
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=polymarket_sdk --cov-report=html

# Run specific test file
pytest tests/test_price_utils.py -v
```

### 5. Run Linting

```bash
# Run pylint
pylint polymarket_sdk

# Run mypy for type checking
mypy polymarket_sdk
```

### 6. Format Code

```bash
# Run black formatter
black polymarket_sdk tests examples
```

## Google Python Style Guide Compliance

This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html):

1. **Naming Conventions**
   - `module_name`
   - `package_name`
   - `ClassName`
   - `method_name`
   - `function_name`
   - `CONSTANT_NAME`
   - `global_var_name`

2. **Docstrings**
   - All modules, classes, and functions have docstrings
   - Using Google-style docstring format
   - Includes Args, Returns, Raises sections

3. **Type Hints**
   - All functions have type hints
   - Using typing module for complex types
   - Type checking with mypy

4. **Code Organization**
   - One class per file (when appropriate)
   - Related functions grouped together
   - Clear separation of concerns

5. **Error Handling**
   - Custom exception classes
   - Explicit error codes
   - Proper exception hierarchy

## Security Considerations

See `SECURITY_ANALYSIS.md` for detailed security analysis and recommendations.

### Key Points:

1. **Never commit private keys** - Use environment variables
2. **Validate all inputs** - Explicit validation with error messages
3. **Use type hints** - Catch errors early with type checking
4. **Sanitize errors** - Don't leak sensitive information
5. **Pin dependencies** - Use specific versions in production

## Testing Guidelines

### Unit Tests

- Test one function at a time
- Use descriptive test names
- Include edge cases
- Test error conditions
- Aim for >80% code coverage

### Example Test Structure:

```python
class TestFunctionName:
    """Tests for function_name."""

    def test_normal_case(self):
        """Test normal operation."""
        result = function_name(valid_input)
        assert result == expected_output

    def test_edge_case(self):
        """Test edge case."""
        result = function_name(edge_input)
        assert result == edge_output

    def test_error_case(self):
        """Test error handling."""
        with pytest.raises(ExpectedError):
            function_name(invalid_input)
```

## Contributing

### Before Committing:

1. Run tests: `pytest`
2. Run linting: `pylint polymarket_sdk`
3. Run type checking: `mypy polymarket_sdk`
4. Format code: `black .`
5. Update documentation if needed

### Commit Message Format:

```
type(scope): subject

body (optional)

BREAKING CHANGE: description (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Next Steps for Implementation

### Priority 1: Core Clients

1. **DataApiClient**
   - HTTP client setup with aiohttp
   - Rate limiting
   - Response caching
   - Error handling

2. **GammaApiClient**
   - Market data fetching
   - Event queries
   - Trending markets

3. **ClobApiClient**
   - Orderbook processing
   - Order placement (stub)
   - Arbitrage detection integration

### Priority 2: Trading Infrastructure

1. **TradingClient**
   - Integration with web3.py
   - Transaction signing
   - Order execution
   - Gas estimation

2. **CTFClient**
   - Smart contract interaction
   - Split/Merge/Redeem operations
   - Balance queries

### Priority 3: Advanced Services

1. **ArbitrageService**
   - Real-time monitoring
   - Execution logic
   - Position management

2. **MarketService**
   - K-line aggregation
   - Signal detection
   - Spread analysis

## Resources

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest Documentation](https://docs.pytest.org/)
- [web3.py Documentation](https://web3py.readthedocs.io/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [Polymarket Documentation](https://docs.polymarket.com/)

## Questions or Issues?

Please refer to the TypeScript SDK documentation for API details and behavior specifications.
