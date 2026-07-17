import hashlib
import hmac
from types import SimpleNamespace

from bot.client import BinanceFuturesClient


def test_build_signature_uses_url_encoded_query_string():
    client = BinanceFuturesClient(api_key="key", api_secret="secret")
    params = {"symbol": "BTCUSDT", "side": "BUY", "price": "100.00"}

    signature = client._build_signature(params)
    expected = hmac.new(
        b"secret",
        b"price=100.00&side=BUY&symbol=BTCUSDT",
        hashlib.sha256,
    ).hexdigest()

    assert signature == expected


def test_post_requests_use_form_data(monkeypatch):
    captured = {}

    def fake_request(method, url, headers=None, params=None, data=None, timeout=None):
        captured["method"] = method
        captured["url"] = url
        captured["headers"] = headers
        captured["params"] = params
        captured["data"] = data
        captured["timeout"] = timeout
        return SimpleNamespace(ok=True, status_code=200, reason="OK", text="{}", json=lambda: {"orderId": 1})

    monkeypatch.setattr("bot.client.requests.request", fake_request)

    client = BinanceFuturesClient(api_key="key", api_secret="secret")
    client._request("POST", "/fapi/v1/order", {"symbol": "BTCUSDT"})

    assert captured["method"] == "POST"
    assert captured["data"] is not None
    assert captured["params"] is None
