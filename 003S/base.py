# base.py - Configuration Manager
import json
import os

def load_config(filepath):
    """Load configuration from JSON file."""
    config = {}
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            config = json.load(f)
    return config

def initialize_app(config_path):
    """Initialize application with configuration."""
    config = load_config(config_path)
    
    # Set up database
    db_config = {
        "host": config.get("db_host", "localhost"),
        "port": config.get("db_port", 5432),
        "name": config.get("db_name", "myapp"),
    }
    connection = create_connection(db_config)
    
    # Set up application settings
    app_settings = {
        "debug": config.get("debug", False),
        "log_level": config.get("log_level", "INFO"),
        "max_retries": config.get("max_retries", 3),
    }
    
    return connection, app_settings

def update_config(config, key, value):
    """Update a configuration value."""
    config[key] = value
    return config