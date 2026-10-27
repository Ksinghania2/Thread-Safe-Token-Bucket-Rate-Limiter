# Thread-Safe Token-Bucket Rate Limiter

A small Python implementation of an in-memory token bucket. It refills tokens from elapsed time, caps the bucket at its configured capacity, and uses a lock around each request check.

## Run the demonstration

```bash
python rate_limiter.py
```

The script creates a bucket with capacity 5 and refill rate 2 tokens per second, then simulates eight requests. `allow_request()` returns `True` when a token is available and `False` when the bucket is empty.

## Scope and limitations

This is a single-process demonstration, not an HTTP service or a DDoS defense. The token state is held in memory and is not shared across processes or machines. The implementation uses `time.time()`, so system clock adjustments can affect refill calculations; a production implementation should use a monotonic clock and define validation, client scoping, and distributed-state behavior.
