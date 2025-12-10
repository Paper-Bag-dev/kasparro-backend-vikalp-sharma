import httpx
import time
from observability.logger import log_json

MAX_RETRIES = 3
BACKOFF_FACTOR = 0.5 


def request_with_retry(method: str, url: str, **kwargs):
    attempt = 0

    while True:
        try:
            response = httpx.request(method, url, **kwargs)

            if response.status_code in {429, 500, 502, 503, 504}:
                raise httpx.HTTPStatusError(
                    "Retryable status",
                    request=response.request,
                    response=response,
                )

            return response
        
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt >= MAX_RETRIES:
                log_json("http_request_failed",
                    level="ERROR",
                    url=url,
                    error=str(e),
                    attempts=attempt + 1
                )
                raise

            sleep_time = BACKOFF_FACTOR * (2 ** attempt)

            log_json("http_retry",
                level="WARNING",
                url=url,
                attempt=attempt + 1,
                wait_seconds=sleep_time,
            )

            time.sleep(sleep_time)
            attempt += 1
