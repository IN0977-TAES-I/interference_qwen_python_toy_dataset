# base.py - Cache Manager
import threading

class CacheManager:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key):
        """Get value from cache."""
        with self._lock:
            return self._cache.get(key)
    
    def set(self, key, value, ttl=None):
        """Set value in cache."""
        with self._lock:
            self._cache[key] = {
                "value": value,
                "ttl": ttl,
            }
    
    def delete(self, key):
        """Delete key from cache."""
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self):
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def get_all_keys(self):
        """Get all cache keys."""
        with self._lock:
            return list(self._cache.keys())