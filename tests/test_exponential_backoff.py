import pytest
import httpx
from observability.http_client import request_with_retry, BACKOFF_FACTOR, MAX_RETRIES


def test_exponential_backoff(monkeypatch, capsys):
    calls = {"n": 0}
    sleep_times = []

    def fake_request(method, url, **kwargs):
        calls["n"] += 1
        raise httpx.HTTPStatusError(
            "Server error",
            request=httpx.Request("GET", url),
            response=httpx.Response(503),
        )

    def fake_sleep(t):
        sleep_times.append(t)

    monkeypatch.setattr(httpx, "request", fake_request)
    monkeypatch.setattr("time.sleep", fake_sleep)

    with pytest.raises(httpx.HTTPStatusError):
        request_with_retry("GET", "http://fake")

    expected = [
        BACKOFF_FACTOR * (2 ** attempt)
        for attempt in range(MAX_RETRIES)
    ]

    assert sleep_times == expected
