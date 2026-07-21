import pytest
from fastapi.testclient import TestClient
from main import app
from src.database import SessionLocal, init_db
from src.models import User, Wallet

client = TestClient(app)

def test_root_health_check():
    """Verify that the engine root health check responds correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "message": "Tridding Engine is fully operational."}

def test_database_seeder():
    """Verify that the default user_123 and $10,000 wallet exist in SQLite."""
    init_db()
    db = SessionLocal()
    user = db.query(User).filter(User.id == "user_123").first()
    wallet = db.query(Wallet).filter(Wallet.user_id == "user_123").first()
    
    assert user is not None
    assert user.email == "trader@tridding.com"
    assert wallet is not None
    assert wallet.available_balance == 10000.00
    db.close()
