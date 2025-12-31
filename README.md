# MANA/USD 15-Minute Candle API

A production-ready FastAPI-based REST API service for fetching and serving MANA/USD cryptocurrency market data with 15-minute intervals from Binance.

## 🚀 Features

- **Real-time Data**: Fetch latest MANA/USD market data from Binance
- **Clean Architecture**: Well-structured code with proper error handling
- **Environment Configuration**: Secure handling of sensitive data via environment variables
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **API Documentation**: Interactive Swagger UI and ReDoc documentation
- **CORS Support**: Cross-origin resource sharing for web applications
- **Error Handling**: Robust error handling with meaningful error messages
- **Type Hints**: Full type annotations for better code maintainability

## 📁 Project Structure

```
manaUSD_15min-api/
├── main.py              # FastAPI main application with endpoints
├── config.py            # Configuration settings and environment variables
├── utils.py             # Utility functions for data fetching and processing
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Environment variables (not in git)
├── .gitignore           # Git ignore file
├── data/               # Local storage directory (empty)
├── README.md           # This file
└── LICENSE             # License file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd manaUSD_15min-api
```

2. **Create and activate a virtual environment**:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration (optional)
```

## ⚙️ Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```env
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=True

# External API URL (optional - for deployment)
API_URL=https://your-deployment-url.com/candles

# Binance API Configuration
BINANCE_BASE_URL=https://api.binance.com/api/v3

# Logging
LOG_LEVEL=INFO

# CORS (add your frontend URLs)
CORS_ORIGINS=http://localhost:3000,https://your-frontend.com
```

## 🚀 Usage

### Start the API Server

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### API Endpoints

| Endpoint | Method | Description | Response |
|----------|---------|-------------|----------|
| `/` | GET | Root endpoint with API info | API status and metadata |
| `/health` | GET | Health check | Health status |
| `/candles` | GET | Latest 15-min MANA/USD candles | Candle data with metadata |
| `/docs` | GET | Interactive API documentation | Swagger UI |
| `/redoc` | GET | Alternative API documentation | ReDoc UI |

### Example Requests

```bash
# Health check
curl http://127.0.0.1:8000/health

# Get API information
curl http://127.0.0.1:8000/

# Get latest candles
curl http://127.0.0.1:8000/candles
```

### Example Response

```json
{
  "symbol": "MANAUSDT",
  "interval": "15m",
  "count": 20,
  "candles": [
    {
      "Open time": "2024-01-15T10:00:00",
      "Open": 0.4500,
      "High": 0.4520,
      "Low": 0.4480,
      "Close": 0.4510,
      "Volume": 125000.0
    }
  ],
  "status": "success"
}
```

## 📚 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔧 Development

### Code Structure

- **main.py**: FastAPI application with routes, middleware, and error handling
- **config.py**: Configuration management with environment variables
- **utils.py**: Data fetching and processing utilities with proper error handling

### Adding New Features

1. **New endpoints**: Add to `main.py` with proper error handling and documentation
2. **Data processing**: Add functions to `utils.py` with type hints and logging
3. **Configuration**: Update `config.py` and `.env.example`

### Code Quality

The project follows Python best practices:

- Type hints for all functions
- Comprehensive docstrings
- Proper error handling
- Logging throughout the application
- Environment-based configuration

## 🐳 Docker (Optional)

Create a `Dockerfile` for containerization:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## 🚀 Deployment

### Environment Variables for Production

Set these environment variables in your production environment:

```bash
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-frontend.com,https://www.your-frontend.com
LOG_LEVEL=INFO
```

### Popular Deployment Platforms

- **Heroku**: Add `Procfile` with `web: python main.py`
- **Railway**: Use the default Python build process
- **DigitalOcean App Platform**: Configure via `app.yaml`
- **AWS Lambda**: Use Mangum adapter for serverless deployment

## 📊 Data Source

Currently uses the Binance public API:
- **Endpoint**: `https://api.binance.com/api/v3/klines`
- **Rate Limits**: 1200 requests per minute
- **Data**: Real-time MANA/USDT trading data

No API key required for public market data.

## 🔒 Security

- Environment variables for sensitive configuration
- CORS properly configured
- Request timeout and retry mechanisms
- Input validation and sanitization
- Comprehensive error handling without exposing internals

## 📝 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://127.0.0.1:8000/docs)
2. Review the logs for error details
3. Ensure all environment variables are properly configured
4. Verify your internet connection for Binance API access

---

**Happy Trading! 📈**