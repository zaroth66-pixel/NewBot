from google import genai
from groq import Groq
import logging

from app.core.config import settings


logger = logging.getLogger(__name__)


class AIProvider:

    def __init__(self):

        self.groq_client = None
        self.gemini_client = None


        if settings.GROQ_API_KEY:

            self.groq_client = Groq(
                api_key=settings.GROQ_API_KEY
            )

            logger.info(
                "Groq AI initialized"
            )

        else:

            logger.warning(
                "GROQ_API_KEY missing"
            )



        if settings.GEMINI_API_KEY:

            self.gemini_client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

            logger.info(
                "Gemini AI initialized"
            )

        else:

            logger.warning(
                "GEMINI_API_KEY missing"
            )



    async def analyze_market_groq(
        self,
        market_data: dict,
        timeframe: str
    ) -> str:


        if not self.groq_client:

            return (
                "❌ Groq AI is not configured."
            )


        try:


            prompt = f"""

You are Selina AI Forex Analyst.

Analyze this market.

Timeframe:
{timeframe}


Market Data:

{market_data}


Return format:

📈 Trend:
(Bullish/Bearish/Sideways)


🎯 Signal:
(BUY/SELL/NO_TRADE)


💰 Entry Zone:


🛑 Stop Loss:


✅ Take Profit:


📊 Confidence:
(0-100%)


⚠️ Risk Management:


Reasoning:
Explain using indicators.

"""


            result = self.groq_client.chat.completions.create(

                model="openai/gpt-oss-120b",


                messages=[

                    {
                        "role": "system",
                        "content":
                        """
You are Selina AI,
a professional forex technical analyst.
Never invent live prices.
Analyze only supplied data.
"""
                    },


                    {
                        "role": "user",
                        "content": prompt
                    }

                ],


                temperature=0.2,


                max_tokens=1200

            )


            if (
                result.choices
                and result.choices[0].message.content
            ):

                return (
                    result
                    .choices[0]
                    .message
                    .content
                )


            return (
                "No AI response received."
            )


        except Exception as e:


            logger.exception(
                "Groq analysis failed"
            )


            return (
                f"❌ Groq Error:\n{str(e)}"
            )





    async def generate_reasoning_gemini(
        self,
        analysis_result: str,
        news_context: str = ""
    ) -> str:


        if not self.gemini_client:

            return (
                "❌ Gemini AI is not configured."
            )


        try:


            prompt = f"""

You are Selina AI.

Explain this forex signal:

{analysis_result}


News:

{news_context}


Give concise professional reasoning.

"""


            response = (
                self.gemini_client
                .models
                .generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            )


            if response.text:

                return response.text


            return (
                "No Gemini response."
            )


        except Exception as e:


            logger.exception(
                "Gemini reasoning failed"
            )


            return (
                f"❌ Gemini Error:\n{str(e)}"
            )




ai_provider = AIProvider()
