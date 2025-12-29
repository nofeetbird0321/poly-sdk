"""Unit tests for core error handling.

Tests for PolymarketError and retry functionality.
"""

import pytest
import asyncio
from polymarket_sdk.core.errors import (
    ErrorCode,
    PolymarketError,
    with_retry,
)


class TestPolymarketError:
    """Tests for PolymarketError class."""

    def test_error_creation(self):
        """Test basic error creation."""
        error = PolymarketError(
            ErrorCode.MARKET_NOT_FOUND,
            "Market not found",
        )
        assert error.code == ErrorCode.MARKET_NOT_FOUND
        assert error.message == "Market not found"
        assert error.retryable is False

    def test_retryable_error(self):
        """Test creating a retryable error."""
        error = PolymarketError(
            ErrorCode.NETWORK_ERROR,
            "Network error",
            retryable=True,
        )
        assert error.retryable is True

    def test_from_http_error_429(self):
        """Test creating error from HTTP 429 (rate limited)."""
        error = PolymarketError.from_http_error(429)
        assert error.code == ErrorCode.RATE_LIMITED
        assert error.retryable is True

    def test_from_http_error_404(self):
        """Test creating error from HTTP 404 (not found)."""
        error = PolymarketError.from_http_error(404)
        assert error.code == ErrorCode.MARKET_NOT_FOUND
        assert error.retryable is False

    def test_from_http_error_500(self):
        """Test creating error from HTTP 500 (server error)."""
        error = PolymarketError.from_http_error(500)
        assert error.code == ErrorCode.NETWORK_ERROR
        assert error.retryable is True

    def test_from_http_error_with_body(self):
        """Test creating error with response body message."""
        body = {"message": "Custom error message"}
        error = PolymarketError.from_http_error(400, body)
        assert "Custom error message" in error.message


class TestWithRetry:
    """Tests for retry functionality."""

    @pytest.mark.asyncio
    async def test_retry_success_first_attempt(self):
        """Test successful execution on first attempt."""
        call_count = 0

        async def success_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await with_retry(success_func, max_retries=3)
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_success_after_failures(self):
        """Test successful execution after some failures."""
        call_count = 0

        async def eventual_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise PolymarketError(
                    ErrorCode.NETWORK_ERROR,
                    "Network error",
                    retryable=True,
                )
            return "success"

        result = await with_retry(eventual_success, max_retries=3, base_delay=0.01)
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retry_non_retryable_error(self):
        """Test that non-retryable errors are not retried."""
        call_count = 0

        async def non_retryable_error():
            nonlocal call_count
            call_count += 1
            raise PolymarketError(
                ErrorCode.MARKET_NOT_FOUND,
                "Market not found",
                retryable=False,
            )

        with pytest.raises(PolymarketError) as exc_info:
            await with_retry(non_retryable_error, max_retries=3)

        assert exc_info.value.code == ErrorCode.MARKET_NOT_FOUND
        assert call_count == 1  # Should not retry

    @pytest.mark.asyncio
    async def test_retry_exhausted(self):
        """Test that retries are exhausted and error is raised."""
        call_count = 0

        async def always_fails():
            nonlocal call_count
            call_count += 1
            raise PolymarketError(
                ErrorCode.NETWORK_ERROR,
                "Network error",
                retryable=True,
            )

        with pytest.raises(PolymarketError):
            await with_retry(always_fails, max_retries=3, base_delay=0.01)

        assert call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
