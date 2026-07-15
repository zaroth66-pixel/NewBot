from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class SubscriptionPlan(str, enum.Enum):
    FREE = "FREE"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"
    LIFETIME = "LIFETIME"

class SignalDirection(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"
    NO_TRADE = "NO_TRADE"

class SignalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED_TP1 = "CLOSED_TP1"
    CLOSED_TP2 = "CLOSED_TP2"
    CLOSED_SL = "CLOSED_SL"
    CANCELLED = "CANCELLED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Preferences
    notify_new_signals = Column(Boolean, default=True)
    notify_tp_sl = Column(Boolean, default=True)
    notify_high_volatility = Column(Boolean, default=False)
    notify_major_news = Column(Boolean, default=False)

    favorites = relationship("Favorite", back_populates="user")
    portfolio = relationship("PortfolioTrade", back_populates="user")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    currency_pair = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    currency_pair = Column(String, index=True, nullable=False)
    direction = Column(Enum(SignalDirection), nullable=False)
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    tp1 = Column(Float, nullable=False)
    tp2 = Column(Float, nullable=True)
    confidence = Column(Float, nullable=False)
    probability = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_reward = Column(Float, nullable=False)
    trade_duration = Column(String, nullable=True)
    ai_reasoning = Column(Text, nullable=False)
    status = Column(Enum(SignalStatus), default=SignalStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

class PortfolioTrade(Base):
    __tablename__ = "portfolio_trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    signal_id = Column(Integer, ForeignKey("signals.id"))
    status = Column(Enum(SignalStatus), default=SignalStatus.ACTIVE)
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="portfolio")
    signal = relationship("Signal")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    provider = Column(String, nullable=False) # "stripe" or "paypal"
    transaction_id = Column(String, unique=True, index=True)
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    status = Column(String, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="payments")