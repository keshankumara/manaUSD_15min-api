"""
Configuration settings for the MANA/USD 15-min Candle API.

This module contains all configuration constants and settings.
Sensitive data is loaded from environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Trading pair configuration
SYMBOL = "MANAUSDT"
INTERVAL = "15m"
LIMIT = 20

# Binance API configuration
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL", "https://api.binance.com/api/v3")
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

# API server configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes", "on")

# External API URL (optional - for deployment)
API_URL: Optional[str] = os.getenv("API_URL")

# Request configuration
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# CORS configuration (configure properly for production)
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

# Add production origins from environment
if os.getenv("CORS_ORIGINS"):
    additional_origins = os.getenv("CORS_ORIGINS").split(",")
    CORS_ORIGINS.extend([origin.strip() for origin in additional_origins])


def get_config_summary() -> dict:
    """
    Get a summary of current configuration (excluding sensitive data).
    
    Returns:
        Dictionary with configuration summary
    """
    return {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT,
        "api_host": API_HOST,
        "api_port": API_PORT,
        "debug": DEBUG,
        "log_level": LOG_LEVEL,
        "has_external_api_url": bool(API_URL),
        "binance_base_url": BINANCE_BASE_URL,
    }