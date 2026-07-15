import pytest
from app.services.ai_provider import AIProvider

@pytest.mark.asyncio
async def test_ai_provider_initialization():
    provider = AIProvider()
    assert provider is not None

@pytest.mark.asyncio
async def test_analyze_market_groq_no_key():
    provider = AIProvider()
    provider.groq_client = None
    result = await provider.analyze_market_groq({}, "1h")
    assert result == "Groq API not configured."