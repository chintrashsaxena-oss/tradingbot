from __future__ import annotations

from types import SimpleNamespace

from cli import main


def test_main_prompts_for_missing_arguments(monkeypatch):
    responses = iter(["BTCUSDT", "BUY", "MARKET", "0.001"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    captured = {}

    def fake_place_order(**kwargs):
        captured.update(kwargs)
        return {"orderId": 1}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

    class FakeService:
        def __init__(self, client):
            self.client = client

        def place_order(self, **kwargs):
            return fake_place_order(**kwargs)

    monkeypatch.setattr("cli.BinanceFuturesClient", FakeClient)
    monkeypatch.setattr("cli.OrderService", FakeService)
    monkeypatch.setattr("cli.configure_logging", lambda: SimpleNamespace(info=lambda *args, **kwargs: None, error=lambda *args, **kwargs: None))

    exit_code = main([])

    assert exit_code == 0
    assert captured["symbol"] == "BTCUSDT"
    assert captured["side"] == "BUY"
    assert captured["order_type"] == "MARKET"
    assert captured["quantity"] == "0.001"
