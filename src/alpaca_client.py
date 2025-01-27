import os
from alpaca_trade_api.rest import REST
from dotenv import load_dotenv

# Load alpaca client environment variables from .env
load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

# Alpaca client initialization
# This client is shared across the app
alpaca_client = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)
