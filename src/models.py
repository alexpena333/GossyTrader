from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# ==========================================
# 1. USER MODEL (The core identity)
# ==========================================

class User(Base):
    """
    Represents a registered user in the platform.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships to link the user to their money and their trades
    wallet = relationship("Wallet", back_populates="owner", uselist=False)
    orders = relationship("Future33Order", back_populates="owner")

# ==========================================
# 2. WALLET MODEL (The financial state)
# ==========================================

class Wallet(Base):
    """
    Holds the real-time financial balances of a User.
    Separates available buying power from money frozen in contracts.
    """
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    available_balance = Column(Float, default=0.0)
    frozen_balance = Column(Float, default=0.0)

    # Relationship linking back to the user
    owner = relationship("User", back_populates="wallet")

# ==========================================
# 3. FUTURE33 ORDER MODEL (The trading ledger)
# ==========================================

class Future33Order(Base):
    """
    Records every Future33 contract placed by the user.
    Tracks the asset, amount risked, target price, and settlement status.
    """
    __tablename__ = "future33_orders"

    order_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    
    asset_symbol = Column(String, index=True)
    amount = Column(Float, nullable=False)
    target_price = Column(Float, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    
    # Status can be: PENDING, WON, LOST, CANCELLED
    status = Column(String, default="PENDING") 
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship linking back to the user
    owner = relationship("User", back_populates="orders")