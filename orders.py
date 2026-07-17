from __future__ import annotations

from decimal import Decimal
from typing import Any

from bot.client import BinanceClientError, BinanceFuturesClient
from bot.validators import ValidationError, validate_order_type, validate_price, validate_quantity, validate_side, validate_symbol


class OrderService:
    def __init__(self, client: BinanceFuturesClient) -> None:
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: str, price: str | None = None) -> dict[str, Any]:
        validated_symbol = validate_symbol(symbol)
        validated_side = validate_side(side)
        validated_order_type = validate_order_type(order_type)
        validated_quantity = validate_quantity(quantity)
        validated_price = validate_price(price)

        if validated_order_type == "LIMIT" and validated_price is None:
            raise ValidationError("Limit orders require a price.")

        try:
            result = self.client.place_order(
                symbol=validated_symbol,
                side=validated_side,
                order_type=validated_order_type,
                quantity=validated_quantity,
                price=validated_price,
            )
        except BinanceClientError as exc:
            raise RuntimeError(str(exc)) from exc

        return result
