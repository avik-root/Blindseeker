"""
Blindseeker v1.0.0 - Configuration Module
==========================================
Centralized configuration management with environment variable support.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    
    # Application
    APP_NAME = "Blindseeker"
    APP_VERSION = "1.0.0"
    APP_CODENAME = "Shadow Protocol"
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'blindseeker-dev-key-change-in-production')
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Tor
    TOR_ENABLED = os.getenv('TOR_ENABLED', 'false').lower() == 'true'
    TOR_SOCKS_HOST = os.getenv('TOR_SOCKS_HOST', '127.0.0.1')
    TOR_SOCKS_PORT = int(os.getenv('TOR_SOCKS_PORT', 9050))
    TOR_CONTROL_PORT = int(os.getenv('TOR_CONTROL_PORT', 9051))
    TOR_CONTROL_PASSWORD = os.getenv('TOR_CONTROL_PASSWORD', '')
    
    # Proxy
    PROXY_ENABLED = os.getenv('PROXY_ENABLED', 'false').lower() == 'true'
    PROXY_FILE = os.getenv('PROXY_FILE', 'proxies.txt')
    PROXY_ROTATION = os.getenv('PROXY_ROTATION', 'true').lower() == 'true'
    
    # Scan Settings
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 50))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 15))
    RATE_LIMIT_PER_SECOND = int(os.getenv('RATE_LIMIT_PER_SECOND', 10))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 2))
    
    # Export
    DEFAULT_EXPORT_FORMAT = os.getenv('DEFAULT_EXPORT_FORMAT', 'json')
    EXPORT_DIR = os.getenv('EXPORT_DIR', 'exports')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'blindseeker.log')
    
    # User Agent Rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    ]


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)
