from decimal import Decimal

import pytest

from bot.validators import ValidationError, validate_order_type, validate_price, validate_quantity, validate_side, validate_symbol


def test_validate_symbol_uppercases_and_checks_format():
    assert validate_symbol("btcusdt") == "BTCUSDT"

    with pytest.raises(ValidationError):
        validate_symbol("")


def test_validate_side_and_order_type():
    assert validate_side("buy") == "BUY"
    assert validate_order_type("limit") == "LIMIT"

    with pytest.raises(ValidationError):
        validate_side("hold")


def test_validate_quantity_and_price():
    assert validate_quantity("0.01") == Decimal("0.01")
    assert validate_price("100") == Decimal("100")
    assert validate_price(None) is None

    with pytest.raises(ValidationError):
        validate_quantity("-1")
