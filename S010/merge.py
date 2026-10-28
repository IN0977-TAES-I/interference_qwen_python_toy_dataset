# merge.py - Connection Pool (MERGED - Has Semantic Conflict!)
import threading
import time
import atexit

class ConnectionPool:
    def __init__(self, max_connections=10, idle_timeout=300):
        self.max_connections = max_connections
        self.idle_timeout = idle_timeout
        self._connections = []
        self._lock = threading.Lock()
        self._initialized = False
        self._cleanup_timer = None
        self._start_cleanup_timer()  # TRAP: Timer starts immediately!
        atexit.register(self.close_all)
    
    def _start_cleanup_timer(self):
        """Start periodic cleanup of idle connections."""
        self._cleanup_timer = threading.Timer(
            self.idle_timeout, self._cleanup_idle
        )
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()
    
    def _ensure_initialized(self):
        """Lazy initialization of connection pool."""
        # TRAP: No lock here! Race condition with cleanup timer!
        if not self._initialized:
            for _ in range(3):
                conn = self._create_connection()
                self._connections.append(conn)  # TRAP: No lock!
            self._initialized = True
    
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
                    conn["active"] = False
            self._connections = active
        # TRAP: Restarts timer even if pool is being closed!
        self._start_cleanup_timer()
    
    def get_connection(self):
        """Get a connection from the pool (lazy init)."""
        self._ensure_initialized()
        # TRAP: Race condition! Between _ensure_initialized()
        # and this lock, cleanup timer could run and clear connections!
        with self._lock:
            if self._connections:
                conn = self._connections.pop()
                if conn["active"]:  # TRAP: Could be False if cleanup ran
                    conn["last_used"] = time.time()
                    return conn
                # Fall through to create new
            return self._create_connection()
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        conn["last_used"] = time.time()
        with self._lock:
            if conn["active"]:
                self._connections.append(conn)
            # TRAP: If conn was cleaned up, it's silently dropped!
            # Caller thinks it was released but it wasn't tracked
    
    def _create_connection(self):
        """Create a new database connection."""
        return {
            "id": id(object()),
            "active": True,
            "created": time.time(),
            "last_used": time.time(),
        }
    
    def close_all(self):
        """Close all connections and stop cleanup timer."""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
        with self._lock:
            for conn in self._connections:
                conn["active"] = False
            self._connections.clear()
            self._initialized = False

class PoolExhaustedError(Exception):
    pass

# TRAP SCENARIO:
# Thread A: get_connection() -> _ensure_initialized() creates conns
# Timer:    _cleanup_idle() runs, marks all conns as inactive
# Thread A: acquires lock, pops conn, checks conn["active"] -> False!
# Thread A: creates new connection (wasted the lazy init)
# Meanwhile, _cleanup_idle restarts its timer even during shutdown!
# Result: Memory leak + wasted resources + potential crash