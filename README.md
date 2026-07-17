# Binance Futures Testnet Trading Bot

A small Python CLI application for placing market and limit orders on Binance Futures Testnet (USDT-M).

## Features

- Place market and limit orders
- Support BUY and SELL sides
- CLI validation for symbol, side, quantity, price, and order type
- Structured logging to console and file
- Clear error handling for API responses

## Setup

1. Create and activate a Binance Futures Testnet account.
2. Generate API key and secret.
3. Create a `.env` file in the project root with:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the CLI:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 30000
```

You can also launch the app through the wrapper entry point:

```bash
python app.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## Notes

- Binance Futures Testnet uses the base URL `https://testnet.binancefuture.com`.
- The bot writes logs to `trading_bot.log` in the project root.
- This project is intentionally simplified and uses the Binance REST API directly.
