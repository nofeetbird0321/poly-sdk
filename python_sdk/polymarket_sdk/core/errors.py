"""Unified error handling for Polymarket SDK.

This module provides custom exception classes and error codes for the Polymarket SDK,
following Google Python style guide conventions.
"""

from enum import Enum
from typing import Optional
import asyncio


class ErrorCode(str, Enum):
    """Error codes for Polymarket SDK operations."""

    # Network errors
    NETWORK_ERROR = "NETWORK_ERROR"
    TIMEOUT = "TIMEOUT"
    RATE_LIMITED = "RATE_LIMITED"

    # Authentication errors
    AUTH_FAILED = "AUTH_FAILED"
    API_KEY_EXPIRED = "API_KEY_EXPIRED"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"

    # Data errors
    MARKET_NOT_FOUND = "MARKET_NOT_FOUND"
    WALLET_NOT_FOUND = "WALLET_NOT_FOUND"
    INVALID_RESPONSE = "INVALID_RESPONSE"

    # Trading errors
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
    ORDER_REJECTED = "ORDER_REJECTED"
    ORDER_FAILED = "ORDER_FAILED"
    MARKET_CLOSED = "MARKET_CLOSED"

    # API errors
    API_ERROR = "API_ERROR"

    # Internal errors
    INTERNAL_ERROR = "INTERNAL_ERROR"


class PolymarketError(Exception):
    """Base exception class for Polymarket SDK errors.

    Attributes:
        code: The error code indicating the type of error.
        message: Human-readable error message.
        retryable: Whether the operation can be retried.
        original_error: The underlying exception if any.
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        retryable: bool = False,
        original_error: Optional[Exception] = None,
    ):
        """Initialize a PolymarketError.

        Args:
            code: The error code.
            message: Human-readable error description.
            retryable: Whether the operation can be retried.
            original_error: The underlying exception if any.
        """
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.original_error = original_error

    @classmethod
    def from_http_error(cls, status: int, body: Optional[dict] = None) -> "PolymarketError":
        """Create error from HTTP response status.

        Args:
            status: HTTP status code.
            body: Optional response body.

        Returns:
            PolymarketError instance with appropriate error code.
        """
        body_message = ""
        if body and isinstance(body, dict) and "message" in body:
            body_message = str(body["message"])

        if status == 429:
            return cls(
                ErrorCode.RATE_LIMITED,
                body_message or "Rate limited",
                retryable=True,
            )
        elif status == 401:
            return cls(
                ErrorCode.AUTH_FAILED,
                body_message or "Authentication failed",
            )
        elif status == 403:
            return cls(
                ErrorCode.AUTH_FAILED,
                body_message or "Forbidden",
            )
        elif status == 404:
            return cls(
                ErrorCode.MARKET_NOT_FOUND,
                body_message or "Resource not found",
            )
        elif status == 400:
            return cls(
                ErrorCode.INVALID_RESPONSE,
                body_message or "Bad request",
            )
        else:
            return cls(
                ErrorCode.NETWORK_ERROR,
                body_message or f"HTTP {status}",
                retryable=status >= 500,
            )


async def with_retry(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0,
):
    """Retry decorator for async functions with exponential backoff.

    Args:
        func: Async function to retry.
        max_retries: Maximum number of retry attempts.
        base_delay: Base delay in seconds between retries.

    Returns:
        The result of the function call.

    Raises:
        The last exception encountered if all retries fail.
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as error:
            last_error = error
            if isinstance(error, PolymarketError) and not error.retryable:
                raise

            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)

    if last_error:
        raise last_error
