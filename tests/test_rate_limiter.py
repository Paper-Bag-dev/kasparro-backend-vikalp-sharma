from observability.rate_limiter import enforce_rate_limit, reset_rate_limiter, RATE_LIMITS


def test_rate_limiter(monkeypatch):
    reset_rate_limiter()
    sleep_times = []

    def fake_sleep(t):
        sleep_times.append(t)

    monkeypatch.setattr("time.sleep", fake_sleep)

    source = "coingecko"
    RATE_LIMITS[source] = 1.0

    enforce_rate_limit(source)

    enforce_rate_limit(source)

    assert len(sleep_times) == 1
    assert 0.9 <= sleep_times[0] <= 1.1 
