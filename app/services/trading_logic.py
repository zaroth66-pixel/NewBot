import pandas as pd
import pandas_ta as ta
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.services.market_data import market_data_provider
from app.services.ai_provider import ai_provider
from app.db.models import SignalDirection

logger = logging.getLogger(__name__)

class TradingLogic:
    def __init__(self):
        self.timeframes = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"]
        
    def _calculate_indicators(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            values = data.get("values", [])
            if not values:
                return {}
                
            # TwelveData returns newest first, so we reverse it for pandas
            df = pd.DataFrame(values[::-1])
            df['datetime'] = pd.to_datetime(df['datetime'])
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col])
                else:
                    df[col] = 0.0 # fallback if no volume
            
            # Set index
            df.set_index('datetime', inplace=True)
            
            # Calculate Indicators
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.ema(length=200, append=True)
            df.ta.rsi(length=14, append=True)
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.bbands(length=20, std=2, append=True)
            df.ta.stoch(append=True)
            
            # Get the latest row
            latest = df.iloc[-1].to_dict()
            
            # Convert timestamp to string if needed or remove it
            return {k: v for k, v in latest.items() if pd.notna(v)}
        except Exception as e:
            logger.error(f"Error calculating indicators: {str(e)}")
            return {}

    async def analyze_and_generate_signal(self, symbol: str) -> Optional[Dict[str, Any]]:
        try:
            # 1. Fetch market data for multiple timeframes
            market_data_summary = {}
            for tf in self.timeframes:
                data = await market_data_provider.get_market_data(symbol, tf)
                if data:
                    indicators = self._calculate_indicators(data)
                    market_data_summary[tf] = indicators
            
            if not market_data_summary:
                logger.error(f"No market data retrieved for {symbol}")
                return None

            # 2. Get AI Analysis via Groq
            groq_analysis = await ai_provider.analyze_market_groq(market_data_summary, "multi-timeframe")
            
            # 3. Parse Groq response to structured data
            signal_data = self._parse_ai_response(groq_analysis)
            
            if not signal_data or signal_data.get("direction") == SignalDirection.NO_TRADE:
                return None

            # 4. Get detailed reasoning via Gemini
            detailed_reasoning = await ai_provider.generate_reasoning_gemini(groq_analysis)
            signal_data["ai_reasoning"] = detailed_reasoning
            
            return signal_data

        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {str(e)}")
            return None
            
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        # Placeholder for parsing logic. 
        # You would typically enforce JSON output from the LLM or use regex.
        # Returning mock data for structure demonstration
        return {
            "direction": SignalDirection.BUY,
            "entry_price": 1.1050,
            "stop_loss": 1.1000,
            "tp1": 1.1100,
            "tp2": 1.1150,
            "confidence": 85.5,
            "probability": 75.0,
            "risk_score": 3.5,
            "risk_reward": 2.0,
            "trade_duration": "4 hours"
        }

trading_logic = TradingLogic()