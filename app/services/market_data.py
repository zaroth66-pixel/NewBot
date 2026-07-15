import httpx
import logging
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class MarketDataProvider:
    def __init__(self):
        self.provider = settings.DEFAULT_DATA_PROVIDER
        self.clients = {
            "twelvedata": self._fetch_twelvedata,
            "finnhub": self._fetch_finnhub,
            "polygon": self._fetch_polygon,
            "alphavantage": self._fetch_alphavantage
        }

    async def get_market_data(self, symbol: str, interval: str) -> Optional[Dict[str, Any]]:
        fetch_func = self.clients.get(self.provider)
        if not fetch_func:
            logger.error(f"Unsupported market data provider: {self.provider}")
            return None
        
        try:
            return await fetch_func(symbol, interval)
        except Exception as e:
            logger.error(f"Error fetching data from {self.provider}: {str(e)}")
            # Implement fallback logic here if needed
            return None

    async def _fetch_twelvedata(self, symbol: str, interval: str) -> Optional[Dict[str, Any]]:
        api_key = settings.TWELVEDATA_API_KEY
        if not api_key:
            logger.warning("TwelveData API key not set")
            return None
            
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={api_key}&outputsize=100"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                if "values" in data:
                    return data
                else:
                    logger.error(f"TwelveData Error: {data}")
                    return None
            except Exception as e:
                logger.error(f"Error fetching from TwelveData: {str(e)}")
                return None

    async def _fetch_finnhub(self, symbol: str, interval: str) -> Optional[Dict[str, Any]]:
        # Implement finnhub specific logic
        pass

    async def _fetch_polygon(self, symbol: str, interval: str) -> Optional[Dict[str, Any]]:
        # Implement polygon specific logic
        pass

    async def _fetch_alphavantage(self, symbol: str, interval: str) -> Optional[Dict[str, Any]]:
        # Implement alphavantage specific logic
        pass

market_data_provider = MarketDataProvider()