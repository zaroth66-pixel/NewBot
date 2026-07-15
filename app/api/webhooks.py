from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
import logging
from datetime import datetime, timedelta

from app.core.config import settings
from app.db.session import get_db
from app.db.models import User, Payment, SubscriptionPlan
from app.bot import run_bot

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        user_id = int(session.get("metadata", {}).get("user_id"))
        plan_str = session.get("metadata", {}).get("plan")
        transaction_id = session.get("id")
        amount = session.get("amount_total") / 100.0 # Convert cents to dollars
        
        # Grant premium to user
        await activate_premium(db, user_id, plan_str, amount, "stripe", transaction_id)
        
    return {"status": "success"}

async def activate_premium(db: AsyncSession, user_id: int, plan_str: str, amount: float, provider: str, transaction_id: str):
    from sqlalchemy.future import select
    
    # Get user
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        logger.error(f"User {user_id} not found during premium activation")
        return
        
    plan = SubscriptionPlan(plan_str)
    
    # Record payment
    payment = Payment(
        user_id=user.id,
        amount=amount,
        provider=provider,
        transaction_id=transaction_id,
        plan=plan
    )
    db.add(payment)
    
    # Update user subscription
    user.subscription_plan = plan
    
    now = datetime.utcnow()
    if plan == SubscriptionPlan.MONTHLY:
        user.subscription_expiry = now + timedelta(days=30)
    elif plan == SubscriptionPlan.QUARTERLY:
        user.subscription_expiry = now + timedelta(days=90)
    elif plan == SubscriptionPlan.YEARLY:
        user.subscription_expiry = now + timedelta(days=365)
    elif plan == SubscriptionPlan.LIFETIME:
        user.subscription_expiry = now + timedelta(days=36500) # Roughly 100 years
        
    await db.commit()
    logger.info(f"Activated {plan} premium for user {user_id}")
    
    # In a real app, notify the user via Telegram here
    # await notify_user_premium_activated(user.telegram_id, plan)