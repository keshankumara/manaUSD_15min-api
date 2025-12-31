import requests
import pandas as pd
from config import SYMBOL, INTERVAL, LIMIT, BINANCE_KLINES_URL

def fetch_candles():
    """Fetch last 15-min candles from Binance"""
    url = f"{BINANCE_KLINES_URL}?symbol={SYMBOL}&interval={INTERVAL}&limit={LIMIT}"
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        "Open time", "Open", "High", "Low", "Close", "Volume",
        "Close time", "Quote asset volume", "Number of trades",
        "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
    ])
    
    df = df[["Open time", "Open", "High", "Low", "Close", "Volume"]]
    
    # Convert numeric columns
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = df[col].astype(float)
    
    # Convert timestamp
    df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
    
    return df.to_dict(orient="records")  # return list of dicts