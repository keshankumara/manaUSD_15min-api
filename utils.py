"""
Utility functions for fetching and processing cryptocurrency market data.

This module contains functions to fetch candle data from Binance API
and process it for the MANA/USD 15-minute interval API.
"""

import logging
from typing import List, Dict, Any, Optional
import requests
import pandas as pd
from requests.exceptions import RequestException, Timeout

from config import SYMBOL, INTERVAL, LIMIT, BINANCE_KLINES_URL

# Configure logging
logger = logging.getLogger(__name__)

# Request timeout in seconds
REQUEST_TIMEOUT = 10


def fetch_candles() -> List[Dict[str, Any]]:
    """
    Fetch the latest 15-minute candles from Binance API with live data.
    Data is converted to Sri Lanka timezone (UTC+5:30).
    
    Returns:
        List of dictionaries containing candle data with columns:
        - Open time: Timestamp of candle open (Sri Lanka time)
        - Open: Opening price
        - High: Highest price
        - Low: Lowest price  
        - Close: Closing price
        - Volume: Trading volume
        
    Raises:
        RequestException: If API request fails
        ValueError: If response data is invalid
        Exception: For other processing errors
    """
    try:
        logger.info(f"Fetching LIVE {LIMIT} candles for {SYMBOL} with {INTERVAL} interval")
        
        # Prepare request parameters - force fresh data
        params = {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT
        }
        
        # Add cache-busting headers to ensure fresh data
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        
        # Make API request with cache-busting
        response = requests.get(
            BINANCE_KLINES_URL,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        raw_data = response.json()
        
        if not raw_data or not isinstance(raw_data, list):
            raise ValueError("Invalid response format from Binance API")
        
        # Process the data
        processed_data = process_candle_data(raw_data)
        
        logger.info(f"Successfully fetched {len(processed_data)} candles")
        return processed_data
        
    except Timeout:
        logger.error("Request timeout while fetching candles")
        raise RequestException("Request timeout while fetching data from Binance")
        
    except RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise RequestException(f"Failed to fetch data from Binance: {str(e)}")
        
    except ValueError as e:
        logger.error(f"Data processing error: {str(e)}")
        raise ValueError(f"Invalid data received from Binance: {str(e)}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception(f"Unexpected error while fetching candles: {str(e)}")


def process_candle_data(raw_data: List[List]) -> List[Dict[str, Any]]:
    """
    Process raw candle data from Binance API into a structured format.
    
    Args:
        raw_data: Raw candle data from Binance API
        
    Returns:
        List of processed candle dictionaries
        
    Raises:
        ValueError: If data format is invalid
    """
    try:
        # Define column names based on Binance API documentation
        columns = [
            "Open time", "Open", "High", "Low", "Close", "Volume",
            "Close time", "Quote asset volume", "Number of trades",
            "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
        ]
        
        # Create DataFrame
        df = pd.DataFrame(raw_data, columns=columns)
        
        # Select only the columns we need
        df = df[["Open time", "Open", "High", "Low", "Close", "Volume"]]
        
        # Convert numeric columns to float
        numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for any NaN values after conversion
        if df[numeric_columns].isna().any().any():
            raise ValueError("Invalid numeric data found in candle data")
        
        # Convert timestamp from milliseconds to datetime (UTC)
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
        
        # Convert to Sri Lanka timezone (UTC+5:30)
        df["Open time"] = df["Open time"] + pd.Timedelta(hours=5, minutes=30)
        
        # Convert to list of dictionaries
        result = df.to_dict(orient="records")
        
        # Format the datetime as ISO string for JSON serialization
        for record in result:
            if isinstance(record["Open time"], pd.Timestamp):
                record["Open time"] = record["Open time"].strftime("%Y-%m-%d %H:%M:%S") + " LKT"
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing candle data: {str(e)}")
        raise ValueError(f"Failed to process candle data: {str(e)}")


def validate_symbol(symbol: str) -> bool:
    """
    Validate if a trading symbol is in correct format.
    
    Args:
        symbol: Trading symbol to validate
        
    Returns:
        True if symbol is valid, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Basic validation - symbol should be alphanumeric and reasonable length
    return symbol.isalnum() and 3 <= len(symbol) <= 20


def validate_interval(interval: str) -> bool:
    """
    Validate if an interval is supported by Binance.
    
    Args:
        interval: Time interval to validate
        
    Returns:
        True if interval is valid, False otherwise
    """
    valid_intervals = [
        "1s", "1m", "3m", "5m", "15m", "30m", "1h", 
        "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"
    ]
    
    return interval in valid_intervals


def detect_trend(candles: List[Dict[str, Any]], periods: int = 5) -> Dict[str, Any]:
    """
    Detect price trend from candle data.
    
    Args:
        candles: List of candle dictionaries
        periods: Number of periods to analyze for trend
        
    Returns:
        Dictionary with trend analysis
    """
    try:
        if len(candles) < periods:
            return {"trend": "INSUFFICIENT_DATA", "confidence": 0, "message": "Not enough data for trend analysis"}
        
        # Get recent closing prices
        recent_closes = [float(candle["Close"]) for candle in candles[-periods:]]
        
        # Calculate trend using linear regression-like approach
        if len(recent_closes) < 2:
            return {"trend": "SIDEWAYS", "confidence": 0, "message": "Insufficient data"}
        
        # Simple trend calculation
        first_close = recent_closes[0]
        last_close = recent_closes[-1]
        price_change = last_close - first_close
        price_change_percent = (price_change / first_close) * 100
        
        # Calculate volatility (standard deviation)
        avg_price = sum(recent_closes) / len(recent_closes)
        variance = sum([(price - avg_price) ** 2 for price in recent_closes]) / len(recent_closes)
        volatility = variance ** 0.5
        
        # Determine trend based on price change and volatility
        threshold = volatility * 0.5  # Dynamic threshold based on volatility
        
        if price_change > threshold:
            trend = "UP"
            confidence = min(95, abs(price_change_percent) * 10)
        elif price_change < -threshold:
            trend = "DOWN" 
            confidence = min(95, abs(price_change_percent) * 10)
        else:
            trend = "SIDEWAYS"
            confidence = max(30, 70 - (volatility / avg_price * 1000))
        
        return {
            "trend": trend,
            "confidence": round(confidence, 2),
            "price_change": round(price_change, 6),
            "price_change_percent": round(price_change_percent, 4),
            "volatility": round(volatility, 6),
            "current_price": last_close,
            "analysis_periods": periods
        }
        
    except Exception as e:
        logger.error(f"Error in trend detection: {str(e)}")
        return {"trend": "ERROR", "confidence": 0, "message": f"Analysis failed: {str(e)}"}