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
from utils import fetch_candles, detect_trend

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
            "candles": "/candles - Get live 15-min candles",
            "trend": "/trend?periods=5 - Get trend analysis",
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
    Get the latest 15-minute candles for MANA/USD with LIVE data from Binance.
    Data is converted to Sri Lanka timezone (UTC+5:30).
    
    Returns:
        Dict containing live candle data with metadata
        
    Raises:
        HTTPException: If data fetching fails
    """
    try:
        import datetime
        logger.info(f"Fetching LIVE candles for {SYMBOL} with {INTERVAL} interval")
        candles = fetch_candles()
        
        # Get current Sri Lanka time
        current_time_utc = datetime.datetime.utcnow()
        current_time_lkt = current_time_utc + datetime.timedelta(hours=5, minutes=30)
        
        return {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "count": len(candles),
            "candles": candles,
            "status": "success",
            "fetched_at": current_time_lkt.strftime("%Y-%m-%d %H:%M:%S") + " LKT",
            "data_source": "Binance API (Live)",
            "timezone": "Sri Lanka (UTC+5:30)"
        }
        
    except Exception as e:
        logger.error(f"Error fetching live candles: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch live candle data: {str(e)}"
        )


@app.get("/trend", response_model=Dict[str, Any])
def get_trend_analysis(periods: int = 5) -> Dict[str, Any]:
    """
    Get trend analysis for MANA/USD based on recent candles.
    
    Args:
        periods: Number of periods to analyze (default: 5)
        
    Returns:
        Dict containing trend analysis and candle data
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        import datetime
        logger.info(f"Performing trend analysis for {SYMBOL} with {periods} periods")
        
        # Validate periods
        if periods < 2 or periods > 50:
            raise HTTPException(
                status_code=400,
                detail="Periods must be between 2 and 50"
            )
        
        candles = fetch_candles()
        trend_analysis = detect_trend(candles, periods)
        
        # Get current Sri Lanka time
        current_time_utc = datetime.datetime.utcnow()
        current_time_lkt = current_time_utc + datetime.timedelta(hours=5, minutes=30)
        
        return {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "trend_analysis": trend_analysis,
            "candles_analyzed": min(len(candles), periods),
            "total_candles": len(candles),
            "status": "success",
            "analyzed_at": current_time_lkt.strftime("%Y-%m-%d %H:%M:%S") + " LKT",
            "data_source": "Binance API (Live)"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in trend analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to perform trend analysis: {str(e)}"
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