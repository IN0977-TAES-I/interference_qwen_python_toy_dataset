# right.py - Connection Pool (Memory Safety Branch)
import threading
import time
import atexit

class ConnectionPool:
    def __init__(self, max_connections=10, idle_timeout=300):
        self.max_connections = max_connections
        self.idle_timeout = idle_timeout
        self._connections = []
        self._lock = threading.Lock()
        self._cleanup_timer = None
        self._start_cleanup_timer()
        atexit.register(self.close_all)
    
    def _start_cleanup_timer(self):
        """Start periodic cleanup of idle connections."""
        self._cleanup_timer = threading.Timer(
            self.idle_timeout, self._cleanup_idle
        )
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()
    
    def _cleanup_idle(self):
        """Remove idle connections to free memory."""
        with self._lock:
            now = time.time()
            active = []
            for conn in self._connections:
                idle_time = now - conn.get("created", now)
                if idle_time < self.idle_timeout:
                    active.append(conn)
                else:
                    conn["active"] = False  # Mark as closed
            self._connections = active
        # Restart timer
        self._start_cleanup_timer()
    
    def get_connection(self):
        """Get a connection from the pool."""
        with self._lock:
            if self._connections:
                conn = self._connections.pop()
                if conn["active"]:
                    return conn
                # Connection was cleaned up, create new one
            return self._create_connection()
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        with self._lock:
            if conn["active"]:
                self._connections.append(conn)
    
    def _create_connection(self):
        """Create a new database connection."""
        return {
            "id": id(object()),
            "active": True,
            "created": time.time(),
        }
    
    def close_all(self):
        """Close all connections and stop cleanup timer."""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
        with self._lock:
            for conn in self._connections:
                conn["active"] = False
            self._connections.clear()

class PoolExhaustedError(Exception):
    pass