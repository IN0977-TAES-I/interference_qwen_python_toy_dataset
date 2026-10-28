# left.py - Cache Manager (Performance Branch)
import threading
import time

class CacheManager:
    def __init__(self, max_size=1000):
        self._cache = {}
        self._lock = threading.Lock()
        self._max_size = max_size
        self._hits = 0
        self._misses = 0
    
    def get(self, key):
        """Get value from cache with stats tracking."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None
            # Check TTL inline for performance
            if entry["ttl"] and time.time() > entry["created"] + entry["ttl"]:
                del self._cache[key]  # Direct mutation - fast!
                self._misses += 1
                return None
            self._hits += 1
            return entry["value"]
    
    def set(self, key, value, ttl=None):
        """Set value in cache with eviction."""
        with self._lock:
            if len(self._cache) >= self._max_size:
                self._evict_oldest()  # Direct mutation!
            self._cache[key] = {
                "value": value,
                "ttl": ttl,
                "created": time.time(),
            }
    
    def _evict_oldest(self):
        """Evict oldest entry (direct mutation for speed)."""
        oldest_key = min(self._cache, key=lambda k: self._cache[k]["created"])
        del self._cache[oldest_key]
    
    def delete(self, key):
        """Delete key from cache."""
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self):
        """Clear all cache and reset stats."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def get_all_keys(self):
        """Get all cache keys."""
        with self._lock:
            return list(self._cache.keys())
    
    def get_stats(self):
        """Get cache hit/miss statistics."""
        return {"hits": self._hits, "misses": self._misses}