# MANA/USD 15min Market Data API

A FastAPI-based REST API service for fetching and serving MANA/USD cryptocurrency market data with 15-minute intervals.

## Features

- **Real-time Data**: Fetch latest MANA/USD market data
- **Historical Data**: Query data for specific date ranges
- **Data Export**: Save data to JSON/CSV formats
- **Technical Indicators**: Basic technical analysis calculations
- **CORS Support**: Enable cross-origin requests
- **Auto Documentation**: Interactive API docs with Swagger UI

## Project Structure

```
manaUSD_15min-api/
├── main.py             # FastAPI main application with endpoints
├── requirements.txt    # Python dependencies
├── config.py          # Configuration constants and settings
├── utils.py           # Helper functions for data fetching and processing
├── data/             # Local storage for CSV/JSON files
├── README.md         # Project documentation
└── LICENSE          # License file
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd manaUSD_15min-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize:
- Trading symbol and interval
- Data source API settings
- Cache duration
- File storage options

## Usage

### Start the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- **GET /**: Root endpoint with API information
- **GET /health**: Health check endpoint
- **GET /data**: Get latest market data
  - Query parameters: `limit` (default: 100), `save` (default: false)
- **GET /data/range**: Get data for date range
  - Query parameters: `start_date`, `end_date` (YYYY-MM-DD), `save` (default: false)

### Example Requests

```bash
# Get latest 50 data points
curl "http://localhost:8000/data?limit=50"

# Get data for specific date range
curl "http://localhost:8000/data/range?start_date=2023-01-01&end_date=2023-01-31"

# Save data to file
curl "http://localhost:8000/data?limit=100&save=true"
```

## API Documentation

Once the server is running, visit:
- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Data Format

Market data responses include:
```json
{
  "symbol": "MANAUSD",
  "interval": "15m",
  "count": 100,
  "data": [
    {
      "timestamp": "2023-12-31T12:00:00",
      "open": 0.4500,
      "high": 0.4520,
      "low": 0.4480,
      "close": 0.4510,
      "volume": 125000.0,
      "close_time": "2023-12-31T12:15:00",
      "quote_volume": 56375.0,
      "trades": 450
    }
  ]
}
```

## Development

### Adding New Features

1. **New endpoints**: Add to `main.py`
2. **Data processing**: Add functions to `utils.py`
3. **Configuration**: Update `config.py`

### Testing

Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Data Sources

Currently configured for sample data generation. To connect to real data sources:

1. Update `DATA_SOURCE_URL` in `config.py`
2. Modify `fetch_market_data()` in `utils.py`
3. Add API keys if required

Popular crypto data sources:
- Binance API
- CoinGecko API
- Alpha Vantage
- CoinMarketCap API

## License

This project is licensed under the terms specified in the LICENSE file.