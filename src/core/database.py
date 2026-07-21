from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==========================================
# 1. DATABASE CONFIGURATION (SQLite)
# ==========================================

SQLALCHEMY_DATABASE_URL = "sqlite:///../data/tridding.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ==========================================
# 2. DEPENDENCY INJECTION FOR API ROUTES
# ==========================================

def get_db():
    """
    Creates a new database session for a request and closes it when finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 3. DATABASE SEEDER (Initial Data)
# ==========================================

def init_db():
    """
    Seeds the database with a default user and wallet if they don't exist yet.
    """
    from .models import User, Wallet
    db = SessionLocal()
    
    # Check if default user already exists
    user = db.query(User).filter(User.id == "user_123").first()
    if not user:
        # Create default user
        new_user = User(id="user_123", email="trader@tridding.com", is_active=True)
        db.add(new_user)
        
        # Create default wallet with $10,000 starting capital
        new_wallet = Wallet(user_id="user_123", available_balance=10000.00, frozen_balance=0.00)
        db.add(new_wallet)
        
        db.commit()
        print(">>> Database seeded successfully: Default user_123 created with $10,000.")
    
    db.close()