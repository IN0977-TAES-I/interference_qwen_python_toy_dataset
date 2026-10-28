# left.py - Connection Pool (Lazy Init Branch)
import threading
import time

class ConnectionPool:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self._connections = []
        self._lock = threading.Lock()
        self._initialized = False
    
    def _ensure_initialized(self):
        """Lazy initialization of connection pool."""
        if not self._initialized:
            # Pre-create minimum connections
            for _ in range(3):
                conn = self._create_connection()
                self._connections.append(conn)
            self._initialized = True
    
    def get_connection(self):
        """Get a connection from the pool (lazy init)."""
        self._ensure_initialized()  # Lazy init on first use
        with self._lock:
            if self._connections:
                conn = self._connections.pop()
                conn["last_used"] = time.time()
                return conn
            if len(self._connections) < self.max_connections:
                return self._create_connection()
        raise PoolExhaustedError("No connections available")
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        conn["last_used"] = time.time()
        with self._lock:
            self._connections.append(conn)
    
    def _create_connection(self):
        """Create a new database connection."""
        return {
            "id": id(object()),
            "active": True,
            "created": time.time(),
            "last_used": time.time(),
        }
    
    def close_all(self):
        """Close all connections."""
        with self._lock:
            for conn in self._connections:
                conn["active"] = False
            self._connections.clear()
            self._initialized = False  # Reset for lazy re-init

class PoolExhaustedError(Exception):
    pass