import pytest
import httpx
from observability.http_client import request_with_retry, MAX_RETRIES


@pytest.mark.asyncio
def test_retry_logic(monkeypatch, capsys):
    """Test that retry wrapper retries correct number of times and logs attempts."""
    calls = {"n": 0}

    def fake_request(method, url, **kwargs):
        calls["n"] += 1
        raise httpx.HTTPStatusError(
            "Server error",
            request=httpx.Request("GET", url),
            response=httpx.Response(500),
        )

    monkeypatch.setattr(httpx, "request", fake_request)

    with pytest.raises(httpx.HTTPStatusError):
        request_with_retry("GET", "https://fake-api.test/data")

    assert calls["n"] == MAX_RETRIES + 1

    output = capsys.readouterr().out
    retry_logs = [line for line in output.splitlines() if "http_retry" in line]

    assert len(retry_logs) == MAX_RETRIES
