"""
Blindseeker v1.0.0 - Rate Limiter
===================================
Token bucket rate limiter with adaptive throttling.
Prevents aggressive scanning and respects platform rate limits.
"""

import time
import threading
from collections import defaultdict


class TokenBucket:
    """Token bucket algorithm for rate limiting."""
    
    def __init__(self, rate, burst):
        self.rate = rate          # tokens per second
        self.burst = burst        # max burst size
        self.tokens = burst       # current tokens
        self.last_time = time.monotonic()
        self.lock = threading.Lock()
    
    def consume(self, tokens=1):
        """Try to consume tokens. Returns True if successful."""
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_time
            self.last_time = now
            
            # Add tokens based on elapsed time
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_for_token(self, tokens=1):
        """Wait until tokens are available, then consume them."""
        while not self.consume(tokens):
            time.sleep(0.05)


class RateLimiter:
    """Per-domain rate limiter with adaptive throttling."""
    
    def __init__(self, default_rate=10, default_burst=20):
        self.default_rate = default_rate
        self.default_burst = default_burst
        self.buckets = {}
        self.throttled_domains = {}
        self.lock = threading.Lock()
        self.stats = defaultdict(lambda: {'requests': 0, 'throttled': 0, 'errors': 0})
    
    def _get_domain(self, url):
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc or parsed.hostname or 'unknown'
        except Exception:
            return 'unknown'
    
    def _get_bucket(self, domain):
        """Get or create a token bucket for a domain."""
        with self.lock:
            if domain not in self.buckets:
                # Check if domain is throttled (slower rate)
                rate = self.throttled_domains.get(domain, self.default_rate)
                burst = max(2, rate * 2)
                self.buckets[domain] = TokenBucket(rate, burst)
            return self.buckets[domain]
    
    def acquire(self, url):
        """Acquire permission to make a request to URL."""
        domain = self._get_domain(url)
        bucket = self._get_bucket(domain)
        bucket.wait_for_token()
        self.stats[domain]['requests'] += 1
    
    def report_throttled(self, url):
        """Report that a request was throttled (429 response)."""
        domain = self._get_domain(url)
        self.stats[domain]['throttled'] += 1
        
        with self.lock:
            # Reduce rate for this domain
            current_rate = self.throttled_domains.get(domain, self.default_rate)
            new_rate = max(0.5, current_rate * 0.5)
            self.throttled_domains[domain] = new_rate
            
            # Reset the bucket with new rate
            self.buckets[domain] = TokenBucket(new_rate, max(2, new_rate * 2))
    
    def report_error(self, url):
        """Report a request error."""
        domain = self._get_domain(url)
        self.stats[domain]['errors'] += 1
    
    def get_stats(self):
        """Get rate limiting statistics."""
        return dict(self.stats)
    
    def reset(self):
        """Reset all rate limiters."""
        with self.lock:
            self.buckets.clear()
            self.throttled_domains.clear()
            self.stats.clear()
