import time
import threading

class TokenBucketRateLimiter:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity          # Maximum tokens the bucket can hold
        self.refill_rate = refill_rate      # Tokens added per second
        self.tokens = capacity            # Start with a full bucket
        self.last_refill = time.time()    # Track the last check-in time
        self.lock = threading.Lock()      # ⚡ INTERVIEW FLEX: Concurrency lock

    def _refill_tokens(self):
        now = time.time()
        elapsed = now - self.last_refill
        
        # Calculate how many tokens accumulated since the last request
        tokens_to_add = elapsed * self.refill_rate
        
        # Update token count without exceeding max bucket capacity
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def allow_request(self):
        # Ensure thread safety so concurrent API requests don't cause race conditions
        with self.lock:
            self._refill_tokens()
            
            # If tokens are available, consume one and permit the traffic
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            
            # Bucket is completely drained; block the request
            return False

# Verification Loop
if __name__ == "__main__":
    # Initialize a limiter: Max capacity of 5 tokens, refills at 2 tokens/sec
    limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=2.0)

    # Simulate a high-velocity burst of 8 rapid concurrent incoming requests
    print("Initiating traffic simulation stream...")
    for i in range(1, 9):
        allowed = limiter.allow_request()
        status = "ALLOWED" if allowed else "BLOCKED (429 Too Many Requests)"
        print(f"Request {i}: {status} | Remaining Tokens: {limiter.tokens:.2f}")
        time.sleep(0.1) # Rapid micro-delay