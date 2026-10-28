# right.py - Cache Manager (Safety Branch)
import threading
import time
import copy

class CacheManager:
    def __init__(self, max_size=1000):
        self._cache = {}
        self._lock = threading.RLock()  # Reentrant lock for safety
        self._max_size = max_size
    
    def get(self, key):
        """Get value from cache (returns copy for safety)."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            # Return a deep copy to prevent external mutation
            return copy.deepcopy(entry["value"])
    
    def set(self, key, value, ttl=None):
        """Set value in cache (stores copy for safety)."""
        with self._lock:
            safe_value = copy.deepcopy(value)
            if len(self._cache) >= self._max_size:
                self._evict_safely()
            self._cache[key] = {
                "value": safe_value,
                "ttl": ttl,
                "created": time.time(),
                "accessed": time.time(),
            }
    
    def _evict_safely(self):
        """Evict oldest entry safely."""
        with self._lock:
            oldest_key = min(
                self._cache,
                key=lambda k: self._cache[k].get("accessed", 0)
            )
            # Create new dict without the key (immutable approach)
            self._cache = {
                k: v for k, v in self._cache.items() if k != oldest_key
            }
    
    def delete(self, key):
        """Delete key from cache."""
        with self._lock:
            self._cache = {
                k: v for k, v in self._cache.items() if k != key
            }
    
    def clear(self):
        """Clear all cache entries."""
        with self._lock:
            self._cache = {}
    
    def get_all_keys(self):
        """Get all cache keys (returns copy)."""
        with self._lock:
            return list(self._cache.keys())
    
    def batch_get(self, keys):
        """Get multiple values at once."""
        with self._lock:
            return {
                key: copy.deepcopy(self._cache[key]["value"])
                for key in keys if key in self._cache
            }