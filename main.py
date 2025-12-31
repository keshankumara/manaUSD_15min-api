from fastapi import FastAPI
from utils import fetch_candles

app = FastAPI(title="ManaUSD 15-min Candle API")

@app.get("/")
def root():
    return {"message": "ManaUSD 15-min Candle API is running"}

@app.get("/candles")
def get_candles():
    """Return last 15-min candles"""
    data = fetch_candles()
    return {"candles": data}