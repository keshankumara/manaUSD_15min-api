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
    Fetch the latest 15-minute candles from Binance API.
    
    Returns:
        List of dictionaries containing candle data with columns:
        - Open time: Timestamp of candle open
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
        logger.info(f"Fetching {LIMIT} candles for {SYMBOL} with {INTERVAL} interval")
        
        # Prepare request parameters
        params = {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT
        }
        
        # Make API request
        response = requests.get(
            BINANCE_KLINES_URL,
            params=params,
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
        
        # Convert timestamp from milliseconds to datetime
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
        
        # Convert to list of dictionaries
        result = df.to_dict(orient="records")
        
        # Format the datetime as ISO string for JSON serialization
        for record in result:
            if isinstance(record["Open time"], pd.Timestamp):
                record["Open time"] = record["Open time"].isoformat()
        
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