from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation


class ValidationError(ValueError):
    """Raised when the CLI input is invalid."""


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.isalnum() or len(symbol) < 2:
        raise ValidationError("Symbol must be a non-empty alphanumeric string.")
    return symbol.upper()


def validate_side(side: str) -> str:
    side_upper = side.upper()
    if side_upper not in {"BUY", "SELL"}:
        raise ValidationError("Side must be BUY or SELL.")
    return side_upper


def validate_order_type(order_type: str) -> str:
    order_type_upper = order_type.upper()
    if order_type_upper not in {"MARKET", "LIMIT"}:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return order_type_upper


def validate_quantity(quantity: str) -> Decimal:
    try:
        value = Decimal(quantity)
    except InvalidOperation as exc:
        raise ValidationError("Quantity must be a valid decimal number.") from exc
    if value <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return value


def validate_price(price: str | None) -> Decimal | None:
    if price is None:
        return None
    try:
        value = Decimal(price)
    except InvalidOperation as exc:
        raise ValidationError("Price must be a valid decimal number.") from exc
    if value <= 0:
        raise ValidationError("Price must be greater than zero.")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures Testnet",
        epilog="Example: python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001",
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="Order side: BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Optional limit order price")
    return parser
