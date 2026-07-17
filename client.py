from __future__ import annotations

import hashlib
import hmac
import os
import time
from decimal import Decimal
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode

import requests
from dotenv import load_dotenv


class BinanceClientError(Exception):
    """Raised when a Binance API request fails."""

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

for dotenv_path in (PROJECT_ROOT / ".env", BASE_DIR / ".env"):
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=False)

if (BASE_DIR / ".env").exists():
    load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceFuturesClient:
    def __init__(self, api_key: str | None = None, api_secret: str | None = None, base_url: str = BASE_URL) -> None:
        self.api_key = api_key or os.getenv("BINANCE_API_KEY", "")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET", "")
        self.base_url = base_url.rstrip("/")

    def _build_signature(self, params: dict[str, Any]) -> str:
        query_string = urlencode(
            [(key, str(params[key])) for key in sorted(params)],
            doseq=True,
            quote_via=quote,
            safe="",
        )
        return hmac.new(self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.api_key or not self.api_secret:
            raise BinanceClientError("API credentials are missing. Set BINANCE_API_KEY and BINANCE_API_SECRET in your environment or .env file.")

        params = dict(params or {})
        params.update({"timestamp": int(time.time() * 1000)})
        params["signature"] = self._build_signature(params)

        headers = {"X-MBX-APIKEY": self.api_key, "Content-Type": "application/x-www-form-urlencoded"}
        try:
            if method.upper() == "POST":
                response = requests.request(method, f"{self.base_url}{path}", headers=headers, data=params, timeout=20)
            else:
                response = requests.request(method, f"{self.base_url}{path}", headers=headers, params=params, timeout=20)
            try:
                payload = response.json()
            except ValueError:
                payload = {"raw": response.text}
            if not response.ok:
                raise requests.HTTPError(f"{response.status_code} {response.reason}", response=response)
        except requests.RequestException as exc:
            raise BinanceClientError(f"Network request failed: {exc}") from exc

        if payload.get("code") is not None and payload.get("code") != 200:
            message = payload.get("msg") or str(payload)
            if payload.get("code") == -2015:
                message = f"{message}. Check the API key, secret, permissions, and IP restrictions for your Binance Futures Testnet account."
            raise BinanceClientError(message)
        return payload

    def place_order(self, symbol: str, side: str, order_type: str, quantity: Decimal, price: Decimal | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": format(quantity, "f"),
        }
        if order_type.upper() == "LIMIT" and price is not None:
            params["price"] = format(price, "f")
            params["timeInForce"] = "GTC"
        return self._request("POST", "/fapi/v1/order", params)
