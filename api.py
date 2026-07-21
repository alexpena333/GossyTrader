from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from src.core.database import init_db
from src.core.ledger import (
    create_user,
    authenticate_user,
    get_account_id,
    deposit_cash,
    setup_auto_deposit,
    process_pending_auto_deposits
)
from src.extensions.sessions import start_trading_session, close_trading_session
from src.extensions.if33 import create_if33_market, place_if33_bet

app = FastAPI(title="Tridding Engine Definitive API Architecture", version="4.0")

@app.on_event("startup")
def boot_infrastructure():
    """Initializes the database schema upon application startup."""
    init_db()

class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class AutoDepositSchema(BaseModel):
    user_id: int
    mode: str
    amount: float
    frequency: str
    start_date: str

class BetPlacementSchema(BaseModel):
    user_id: int
    market_id: int
    chosen_option: str
    amount: float

@app.get("/health")
def health_check():
    """System health check endpoint."""
    return {"status": "healthy", "service": "tridding-api"}

@app.post("/api/v1/users/register")
def register(data: UserRegisterSchema):
    """Registers a new user and provisions default accounts."""
    try:
        return create_user(data.username, data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/accounts/auto-deposit")
def schedule_auto_deposit(data: AutoDepositSchema):
    """Sets up a custom automated recurring deposit schedule."""
    try:
        acc_id = get_account_id(data.user_id, data.mode)
        return setup_auto_deposit(acc_id, Decimal(str(data.amount)), data.frequency, data.start_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/cron/process-deposits")
def trigger_cron_deposits():
    """Triggers due batch automated deposits."""
    try:
        process_pending_auto_deposits()
        return {"status": "batch processing completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sessions/close")
def close_session(user_id: int, mode: str):
    """Closes an active trading session and calculates performance matrices."""
    try:
        acc_id = get_account_id(user_id, mode)
        return close_trading_session(acc_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/if33/bet")
def place_bet(data: BetPlacementSchema):
    """Places a prediction bet inside the IF33 binary market framework."""
    try:
        return place_if33_bet(data.user_id, data.market_id, data.chosen_option, Decimal(str(data.amount)))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))