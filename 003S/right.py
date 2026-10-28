# right.py - Configuration Manager (Multi-Environment Branch)
import json
import os

ENVIRONMENTS = {
    "development": "config.dev.json",
    "staging": "config.staging.json",
    "production": "config.prod.json",
}

def load_config(filepath):
    """Load configuration from JSON file with env override."""
    env = os.environ.get("APP_ENV", "development")
    config = {}
    
    # Load base config
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            config = json.load(f)
    
    # Override with environment-specific config
    env_file = ENVIRONMENTS.get(env, filepath)
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            env_config = json.load(f)
            config.update(env_config)
    
    return config

def initialize_app(config_path):
    """Initialize application with configuration."""
    config = load_config(config_path)
    
    # Set up database with environment-aware config
    db_config = {
        "host": config.get("db_host", "localhost"),
        "port": config.get("db_port", 5432),
        "name": config.get("db_name", "myapp"),
        "ssl": config.get("db_ssl", False),  # New: SSL support
        "pool_size": config.get("pool_size", 5),  # New: connection pool
    }
    connection = create_connection(db_config)
    
    # Set up application settings
    app_settings = {
        "debug": config.get("debug", False),
        "log_level": config.get("log_level", "INFO"),
        "max_retries": config.get("max_retries", 3),
        "cache_ttl": config.get("cache_ttl", 300),  # New: cache config
    }
    
    return connection, app_settings

def update_config(config, key, value):
    """Update a configuration value (read-only in production)."""
    env = os.environ.get("APP_ENV", "development")
    if env == "production":
        raise PermissionError("Cannot modify config in production")
    config[key] = value
    return config