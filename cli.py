from __future__ import annotations

import sys
from typing import Sequence

from bot.logging_config import configure_logging
from bot.orders import OrderService
from bot.client import BinanceFuturesClient
from bot.validators import ValidationError, build_parser


def _prompt_for_value(name: str, prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print(f"{name} is required. Please provide a value.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    argv_list = list(sys.argv[1:] if argv is None else argv)

    if argv_list and any(arg in {"-h", "--help"} for arg in argv_list):
        parser.parse_args(argv_list)
        return 0

    args, unknown = parser.parse_known_args(argv_list)
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")

    if args.symbol is None:
        args.symbol = _prompt_for_value("symbol", "Enter symbol (e.g. BTCUSDT): ")
    if args.side is None:
        args.side = _prompt_for_value("side", "Enter side (BUY/SELL): ")
    if args.order_type is None:
        args.order_type = _prompt_for_value("order type", "Enter order type (MARKET/LIMIT): ")
    if args.quantity is None:
        args.quantity = _prompt_for_value("quantity", "Enter quantity: ")
    if args.order_type and args.order_type.upper() == "LIMIT" and args.price is None:
        args.price = _prompt_for_value("price", "Enter price: ")

    logger = configure_logging()

    try:
        client = BinanceFuturesClient()
        service = OrderService(client)
        result = service.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as exc:
        logger.error("Input validation failed: %s", exc)
        parser.error(str(exc))
        return 2
    except RuntimeError as exc:
        logger.error("Order placement failed: %s", exc)
        print(f"Error: {exc}")
        return 1

    logger.info("Order placed successfully: %s", result)
    print("Order placed successfully.")
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
