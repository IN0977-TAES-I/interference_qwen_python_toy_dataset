# left.py - Authentication Module (Testing Branch)
import hashlib
import time
import os

# Flag for testing environment
is_testing = os.environ.get("TESTING", "false") == "true"

def authenticate_user(username, password):
    """Authenticate user with username and password."""
    # Skip auth in testing mode
    if is_testing:
        return True
    
    stored_hash = get_password_hash(username)
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if input_hash == stored_hash:
        log_access(username, "login_success")
        return True
    else:
        log_access(username, "login_failed")
        return False

def get_password_hash(username):
    """Retrieve stored password hash from database."""
    if is_testing:
        return "test_hash_placeholder"
    db = get_database_connection()
    result = db.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )
    return result.fetchone()[0]

def check_access(user_role, required_permission):
    """Check if user has required permission."""
    if is_testing:
        return True  # Allow all in testing
    permissions = get_role_permissions(user_role)
    if required_permission in permissions:
        return True
    return False

def log_access(username, event):
    """Log authentication events."""
    if is_testing:
        return  # Skip logging in tests
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("auth.log", "a") as f:
        f.write(f"[{timestamp}] {username}: {event}\n")