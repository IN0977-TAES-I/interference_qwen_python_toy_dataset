# merge.py - Cache Manager (MERGED - Has Semantic Conflict!)
import threading
import time
import copy

class CacheManager:
    def __init__(self, max_size=1000):
        self._cache = {}
        self._lock = threading.Lock()  # TRAP: Uses Lock not RLock
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
            # TRAP: Checks TTL and mutates directly, but returns
            # the actual reference, not a copy!
            if entry["ttl"] and time.time() > entry["created"] + entry["ttl"]:
                del self._cache[key]
                self._misses += 1
                return None
            self._hits += 1
            # TRAP: Returns reference to cached value!
            # Caller can mutate it and corrupt the cache!
            return entry["value"]
    
    def set(self, key, value, ttl=None):
        """Set value in cache with eviction."""
        with self._lock:
            # TRAP: Stores copy (from right) but get() returns reference
            # This inconsistency means mutations to returned values
            # don't affect cache, but caller thinks they will!
            safe_value = copy.deepcopy(value)
            if len(self._cache) >= self._max_size:
                self._evict_oldest()  # Uses left's fast version
            self._cache[key] = {
                "value": safe_value,
                "ttl": ttl,
                "created": time.time(),
            }
    
    def _evict_oldest(self):
        """Evict oldest entry (direct mutation)."""
        # TRAP: Called while holding self._lock from set()
        # But uses threading.Lock (not RLock) - would deadlock
        # if _evict_oldest tried to acquire the lock again!
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
    
    def batch_get(self, keys):
        """Get multiple values at once."""
        with self._lock:
            # TRAP: Returns copies here but get() returns references!
            # Inconsistent behavior between single and batch access
            return {
                key: copy.deepcopy(self._cache[key]["value"])
                for key in keys if key in self._cache
            }