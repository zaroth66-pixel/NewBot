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

        self.gemini_client = (
            genai.Client(api_key=settings.GEMINI_API_KEY)
            if settings.GEMINI_API_KEY
            else None
        )


    async def analyze_market_groq(
        self,
        market_data: dict,
        timeframe: str
    ) -> str:

        if not self.groq_client:
            logger.warning("Groq API key not configured")
            return "Groq API not configured."


        try:

            prompt = (
                f"""
Analyze this forex market as a professional trading AI.

Timeframe: {timeframe}

Market Data:
{market_data}

Provide:

📈 Trend:
(Bullish/Bearish/Sideways)

🎯 Signal:
(BUY/SELL/NO_TRADE)

💰 Entry Zone:

🛑 Stop Loss:

✅ Take Profit:

📊 Confidence:

⚠️ Risk Management:

Explain your reasoning briefly.
"""
            )


            chat_completion = self.groq_client.chat.completions.create(

                model="openai/gpt-oss-120b",

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are Selina AI, an advanced forex "
                            "market analysis assistant."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.2,

                max_tokens=1200

            )


            return (
                chat_completion
                .choices[0]
                .message
                .content
            )


        except Exception as e:

            logger.error(
                f"Error calling Groq API: {str(e)}"
            )

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
                f"""
Explain this forex analysis:

{analysis_result}

News context:
{news_context}

Give professional reasoning.
"""
            )


            response = self.gemini_client.models.generate_content(

                model="gemini-2.0-flash",

                contents=prompt

            )


            return response.text


        except Exception as e:

            logger.error(
                f"Error calling Gemini API: {str(e)}"
            )

            return f"Error: {str(e)}"



ai_provider = AIProvider()
