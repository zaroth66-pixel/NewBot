import stripe
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    def __init__(self):
        self.prices = {
            "MONTHLY": {"amount": 1999, "currency": "usd"}, # $19.99
            "QUARTERLY": {"amount": 4999, "currency": "usd"}, # $49.99
            "YEARLY": {"amount": 14999, "currency": "usd"}, # $149.99
            "LIFETIME": {"amount": 49999, "currency": "usd"} # $499.99
        }

    def create_stripe_checkout_session(self, user_id: int, plan: str) -> Optional[str]:
        if not settings.STRIPE_API_KEY:
            logger.error("Stripe API key not configured")
            return None
            
        if plan not in self.prices:
            logger.error(f"Invalid subscription plan: {plan}")
            return None
            
        price_info = self.prices[plan]
        
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': price_info['currency'],
                        'product_data': {
                            'name': f'Forex Bot Premium - {plan}',
                        },
                        'unit_amount': price_info['amount'],
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{settings.WEBHOOK_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.WEBHOOK_URL}/payment/cancel",
                client_reference_id=str(user_id),
                metadata={
                    "user_id": user_id,
                    "plan": plan
                }
            )
            return session.url
        except Exception as e:
            logger.error(f"Error creating Stripe session: {str(e)}")
            return None

payment_service = PaymentService()