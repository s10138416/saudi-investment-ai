from app.services.sahmk.parsers import extract_quote_price, summarize_payload


def test_extract_quote_price_from_documented_payload():
    quote = {"symbol": "2222", "price": 25.26, "is_delayed": False}
    assert extract_quote_price(quote) == 25.26


def test_extract_quote_price_does_not_fabricate_value():
    assert extract_quote_price({"symbol": "2222"}) is None
    assert extract_quote_price({"price": None}) is None


def test_summarize_payload_hides_values_and_reports_shape():
    summary = summarize_payload({"symbol": "2222", "price": 25.26, "events": []})
    assert summary["type"] == "object"
    assert summary["symbol"] == "2222"
    assert "keys" in summary
    assert "price" in summary["keys"]
    assert "price_value" not in summary
