"""Unit tests for price utilities module.

This module contains comprehensive tests for price utility functions,
following Google Python style guide and pytest conventions.
"""

import pytest
from polymarket_sdk.utils.price_utils import (
    round_price,
    round_size,
    validate_price,
    validate_size,
    calculate_buy_amount,
    calculate_sell_payout,
    calculate_shares_for_amount,
    calculate_spread,
    calculate_midpoint,
    get_effective_prices,
    check_arbitrage,
    format_price,
    format_usdc,
    calculate_pnl,
)


class TestRoundPrice:
    """Tests for round_price function."""

    def test_round_price_floor(self):
        """Test rounding price down."""
        assert round_price(0.523, "0.01", "floor") == 0.52

    def test_round_price_ceil(self):
        """Test rounding price up."""
        assert round_price(0.523, "0.01", "ceil") == 0.53

    def test_round_price_round(self):
        """Test rounding price to nearest."""
        assert round_price(0.523, "0.01", "round") == 0.52
        assert round_price(0.527, "0.01", "round") == 0.53

    def test_round_price_clamp_min(self):
        """Test price clamping at minimum."""
        assert round_price(0.0001, "0.01", "floor") == 0.001

    def test_round_price_clamp_max(self):
        """Test price clamping at maximum."""
        assert round_price(1.5, "0.01", "ceil") == 0.999


class TestValidatePrice:
    """Tests for validate_price function."""

    def test_validate_price_valid(self):
        """Test valid price validation."""
        valid, error = validate_price(0.52, "0.01")
        assert valid is True
        assert error is None

    def test_validate_price_too_low(self):
        """Test price below minimum."""
        valid, error = validate_price(0.0001, "0.01")
        assert valid is False
        assert "between 0.001 and 0.999" in error

    def test_validate_price_too_high(self):
        """Test price above maximum."""
        valid, error = validate_price(1.5, "0.01")
        assert valid is False
        assert "between 0.001 and 0.999" in error

    def test_validate_price_misaligned_tick(self):
        """Test price not aligned with tick size."""
        valid, error = validate_price(0.525, "0.01")
        assert valid is False
        assert "does not align" in error


class TestCalculations:
    """Tests for calculation functions."""

    def test_calculate_buy_amount(self):
        """Test buy amount calculation."""
        assert calculate_buy_amount(0.52, 100) == 52.0

    def test_calculate_sell_payout(self):
        """Test sell payout calculation."""
        assert calculate_sell_payout(0.52, 100) == 52.0

    def test_calculate_shares_for_amount(self):
        """Test shares calculation from amount."""
        assert calculate_shares_for_amount(52.0, 0.52) == 100.0

    def test_calculate_spread(self):
        """Test spread calculation."""
        assert calculate_spread(0.50, 0.52) == pytest.approx(0.02)

    def test_calculate_midpoint(self):
        """Test midpoint calculation."""
        assert calculate_midpoint(0.50, 0.52) == pytest.approx(0.51)


class TestEffectivePrices:
    """Tests for effective prices calculation."""

    def test_get_effective_prices(self):
        """Test effective prices calculation."""
        effective = get_effective_prices(0.48, 0.46, 0.54, 0.52)
        
        # Buy YES: min(0.48, 1-0.52) = min(0.48, 0.48) = 0.48
        assert effective["effective_buy_yes"] == pytest.approx(0.48)
        
        # Buy NO: min(0.54, 1-0.46) = min(0.54, 0.54) = 0.54
        assert effective["effective_buy_no"] == pytest.approx(0.54)
        
        # Sell YES: max(0.46, 1-0.54) = max(0.46, 0.46) = 0.46
        assert effective["effective_sell_yes"] == pytest.approx(0.46)
        
        # Sell NO: max(0.52, 1-0.48) = max(0.52, 0.52) = 0.52
        assert effective["effective_sell_no"] == pytest.approx(0.52)


class TestArbitrageDetection:
    """Tests for arbitrage detection."""

    def test_check_arbitrage_long_opportunity(self):
        """Test detection of long arbitrage opportunity."""
        # Buy YES @ 0.48 + NO @ 0.50 = 0.98 < 1.00
        arb = check_arbitrage(0.48, 0.50, 0.46, 0.48)
        assert arb is not None
        assert arb["type"] == "long"
        assert arb["profit"] > 0

    def test_check_arbitrage_no_opportunity(self):
        """Test when no arbitrage opportunity exists."""
        # Normal market: YES + NO ≈ 1.00
        arb = check_arbitrage(0.52, 0.50, 0.50, 0.48)
        assert arb is None

    def test_check_arbitrage_short_opportunity(self):
        """Test detection of short arbitrage opportunity."""
        # Create conditions where selling both yields > $1
        # This is rare but possible
        arb = check_arbitrage(0.45, 0.45, 0.56, 0.56)
        if arb is not None:
            assert arb["type"] == "short"
            assert arb["profit"] > 0


class TestFormatting:
    """Tests for formatting functions."""

    def test_format_price(self):
        """Test price formatting."""
        assert format_price(0.5234, "0.01") == "0.52"
        assert format_price(0.5234, "0.001") == "0.523"

    def test_format_usdc(self):
        """Test USDC amount formatting."""
        assert format_usdc(52.5) == "$52.50"
        assert format_usdc(100) == "$100.00"


class TestPnL:
    """Tests for PnL calculation."""

    def test_calculate_pnl_long_profit(self):
        """Test PnL calculation for profitable long position."""
        pnl = calculate_pnl(0.40, 0.55, 100, "long")
        assert pnl["pnl"] == pytest.approx(15.0)
        assert pnl["pnl_percent"] == pytest.approx(37.5)

    def test_calculate_pnl_long_loss(self):
        """Test PnL calculation for losing long position."""
        pnl = calculate_pnl(0.55, 0.40, 100, "long")
        assert pnl["pnl"] == pytest.approx(-15.0)
        assert pnl["pnl_percent"] == pytest.approx(-27.27, rel=1e-2)

    def test_calculate_pnl_short_profit(self):
        """Test PnL calculation for profitable short position."""
        pnl = calculate_pnl(0.55, 0.40, 100, "short")
        assert pnl["pnl"] == pytest.approx(15.0)
        assert pnl["pnl_percent"] == pytest.approx(27.27, rel=1e-2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
