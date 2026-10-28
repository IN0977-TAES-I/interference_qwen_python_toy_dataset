# merge.py - Configuration Manager (MERGED - Has Semantic Conflict!)
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
    
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            config = json.load(f)
    
    # Environment override
    env_file = ENVIRONMENTS.get(env, filepath)
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            env_config = json.load(f)
            config.update(env_config)
    
    # TRAP: User preference defaults added AFTER env override
    # This means env config can be overwritten by defaults!
    config.setdefault("theme", "light")
    config.setdefault("language", "en")
    config.setdefault("notifications", True)
    return config

def initialize_app(config_path):
    """Initialize application with configuration."""
    config = load_config(config_path)
    
    # Set up database with environment-aware config
    db_config = {
        "host": config.get("db_host", "localhost"),
        "port": config.get("db_port", 5432),
        "name": config.get("db_name", "myapp"),
        "ssl": config.get("db_ssl", False),
        "pool_size": config.get("pool_size", 5),
    }
    connection = create_connection(db_config)
    
    # TRAP: config is reassigned to user preferences only!
    # All database/app settings are lost from 'config' variable
    config = {
        "theme": config.get("theme", "light"),
        "language": config.get("language", "en"),
        "notifications": config.get("notifications", True),
        "font_size": config.get("font_size", 14),
    }
    
    # TRAP: Returns user prefs as app_settings - caller expects
    # debug, log_level, max_retries, cache_ttl but gets theme, language!
    return connection, config

def update_config(config, key, value):
    """Update a configuration value and persist."""
    # TRAP: Production check from right is missing because left
    # branch didn't have it - merge kept left's version
    config[key] = value
    save_config(config)
    return config

def save_config(config):
    """Save configuration to file."""
    # TRAP: Always saves to same file regardless of environment!
    with open("user_config.json", "w") as f:
        json.dump(config, f)