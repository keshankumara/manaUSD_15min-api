"""
MANA/USD 15-min Candle API

A FastAPI-based REST API service for fetching MANA/USD cryptocurrency 
market data with 15-minute intervals from Binance.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, Any

from config import SYMBOL, INTERVAL
from utils import fetch_candles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MANA/USD 15-min Candle API",
    description="REST API for fetching MANA/USD cryptocurrency market data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Dict[str, Any])
def root() -> Dict[str, Any]:
    """
    Root endpoint - API health check and basic information.
    
    Returns:
        Dict containing API status and information
    """
    return {
        "message": "MANA/USD 15-min Candle API is running",
        "status": "healthy",
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "endpoints": {
            "candles": "/candles",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict containing health status
    """
    return {"status": "healthy"}


@app.get("/candles", response_model=Dict[str, Any])
def get_candles() -> Dict[str, Any]:
    """
    Get the latest 15-minute candles for MANA/USD.
    
    Returns:
        Dict containing candle data with metadata
        
    Raises:
        HTTPException: If data fetching fails
    """
    try:
        logger.info(f"Fetching candles for {SYMBOL} with {INTERVAL} interval")
        candles = fetch_candles()
        
        return {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "count": len(candles),
            "candles": candles,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error fetching candles: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch candle data: {str(e)}"
        )


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "status": "error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT, DEBUG
    
    logger.info(f"Starting MANA/USD 15-min Candle API on {API_HOST}:{API_PORT}")
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )