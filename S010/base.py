# base.py - Connection Pool
import threading
import time

class ConnectionPool:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self._connections = []
        self._lock = threading.Lock()
    
    def get_connection(self):
        """Get a connection from the pool."""
        with self._lock:
            if self._connections:
                return self._connections.pop()
            if len(self._connections) < self.max_connections:
                return self._create_connection()
        raise PoolExhaustedError("No connections available")
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        with self._lock:
            self._connections.append(conn)
    
    def _create_connection(self):
        """Create a new database connection."""
        return {"id": id(object()), "active": True, "created": time.time()}
    
    def close_all(self):
        """Close all connections."""
        with self._lock:
            for conn in self._connections:
                conn["active"] = False
            self._connections.clear()

class PoolExhaustedError(Exception):
    pass