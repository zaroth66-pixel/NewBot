from google import genai
from groq import Groq
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIProvider:
    def __init__(self):
        self.groq_client = (
            Groq(api_key=settings.GROQ_API_KEY)
            if settings.GROQ_API_KEY
            else None
        )

        if settings.GEMINI_API_KEY:
            self.gemini_client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )
        else:
            self.gemini_client = None


    async def analyze_market_groq(self, market_data: dict, timeframe: str) -> str:
        if not self.groq_client:
            logger.warning("Groq API key not configured")
            return "Groq API not configured."

        try:
            prompt = (
                f"Analyze the following forex market data for timeframe {timeframe} "
                f"and provide a trading signal (BUY, SELL, or NO_TRADE) "
                f"with entry, stop loss, and take profit levels. "
                f"Data: {market_data}"
            )

            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert forex trader AI. "
                            "Analyze technical data and provide actionable trading signals."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.2,
                max_tokens=1000,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            return f"Error: {str(e)}"


    async def generate_reasoning_gemini(
        self,
        analysis_result: str,
        news_context: str = ""
    ) -> str:

        if not self.gemini_client:
            logger.warning("Gemini API key not configured")
            return "Gemini API not configured."

        try:
            prompt = (
                f"Provide detailed reasoning for this technical analysis result: "
                f"{analysis_result}. "
                f"Consider this news context if relevant: {news_context}"
            )

            response = self.gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return f"Error: {str(e)}"


ai_provider = AIProvider()
