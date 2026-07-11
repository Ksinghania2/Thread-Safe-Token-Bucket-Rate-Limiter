# Thread-Safe Token-Bucket Traffic Rate Limiter Engine

A high-performance system middleware utility engineered in Python to implement network traffic shaping and defend API infrastructures against high-velocity traffic spikes and Distributed Denial of Service (DDoS) vectors.

The engine uses the Token-Bucket optimization algorithm, combining a dynamic time-based token replenishment mechanism with strict mutex-driven concurrency boundaries. This ensures low-overhead request filtering across highly concurrent application runtime environments.

## Architectural Framework

1. Dynamic Mathematical Refill: Instead of relying on rigid, resource-heavy background worker clock threads to add tokens, the engine evaluates token generation lazily during incoming request intervals using elapsed epoch timestamp changes.

2. Atomic Concurrency Controls: Enforces structural thread isolation using primitive Mutex locks (`threading.Lock`). This prevents race conditions, ensuring token evaluations remain perfectly linear when multiple connection streams hit the backend simultaneously.

3. Burst Tolerance with Sustained Throttling: The architectural constraints naturally accommodate legitimate high-velocity burst sequences up to the maximum capacity limit while strictly enforcing down-scaling rules during prolonged over-capacity usage.

* **`self.lock = threading.Lock()`**: This creates a guard rail. When 50 requests hit the server at the exact same millisecond, `with self.lock:` forces them to form a single-file line. This completely prevents data corruption or two requests stealing the same token.
* **`elapsed = now - self.last_refill`**: Instead of running a heavy background clock that ticks every second and wastes CPU power, the engine calculates the time *lazily*. It only calculates how much time has passed the exact moment a user knocks on the door.
* **`self.tokens = min(self.capacity, ...)`**: This ensures the bucket has a maximum limit. If no one calls the API for an hour, the tokens don't stack up infinitely—they cap out neatly at your maximum `capacity` (e.g., 5).

## Deployment and Verification

Execute the standalone network safety simulation via the command line interface:

```bash
python3 rate_limiter.py