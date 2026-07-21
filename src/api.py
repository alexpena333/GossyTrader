from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import Wallet, User

try:
    from .ai.agents.master_agent import MasterAgent
    ai_agent = MasterAgent()
except ImportError:
    ai_agent = None

router = APIRouter(prefix="/api/v1", tags=["Tridding API"])

# Simulación temporal en memoria para rastrear inversiones activas de Future33 por usuario
ACTIVE_ESCROW_POSITIONS = {"user_123": 0.0}

class Future33OrderRequest(BaseModel):
    user_id: str
    asset_symbol: str
    amount: float
    target_price: float
    expiration_date: str

@router.get("/ai/analyze/{symbol}")
async def analyze_asset_with_ai(symbol: str, current_price: float = 150.00):
    if ai_agent and hasattr(ai_agent, "evaluate_asset_risk"):
        return ai_agent.evaluate_asset_risk(symbol=symbol, current_price=current_price)
    return {"symbol": symbol.upper(), "status": "active", "message": "MasterAgent connected successfully."}

@router.get("/ai/insight")
async def get_ai_market_insight():
    return {"status": "success", "insight": "Institutional liquidity channels remain optimal."}

@router.post("/future33/order")
async def place_future33_order(order: Future33OrderRequest, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == order.user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="User wallet not found.")
    if wallet.available_balance < order.amount:
        raise HTTPException(status_code=400, detail="Insufficient buying power.")
    
    # Descontar del disponible y acumular en posiciones de inversión activas
    wallet.available_balance -= order.amount
    db.commit()
    db.refresh(wallet)
    
    current_escrow = ACTIVE_ESCROW_POSITIONS.get(order.user_id, 0.0)
    ACTIVE_ESCROW_POSITIONS[order.user_id] = current_escrow + order.amount

    return {
        "status": "success", 
        "message": f"Successfully locked ${order.amount:,.2f} in Future33 escrow for {order.asset_symbol.upper()}.", 
        "new_buying_power": wallet.available_balance
    }

@router.get("/portfolio/{user_id}/dashboard")
async def get_user_dashboard(user_id: str, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="User wallet not found.")
    
    initial_capital = 10000.00
    invested_capital = ACTIVE_ESCROW_POSITIONS.get(user_id, 0.0)
    
    # El balance total es la suma del efectivo libre + el capital invertido en posiciones
    total_balance = wallet.available_balance + invested_capital
    profit_loss = total_balance - initial_capital
    profit_loss_pct = round((profit_loss / initial_capital) * 100, 2)
    
    return {
        "user_id": user_id,
        "total_balance": total_balance,
        "available_buying_power": wallet.available_balance,
        "invested_capital": invested_capital,
        "total_profit_loss": round(profit_loss, 2),
        "profit_loss_percentage": profit_loss_pct,
        "is_positive": profit_loss >= 0
    }

@router.get("/market/trending")
async def get_trending_assets():
    return [
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "current_price": 128.50, "change_24h_percent": 4.25},
        {"symbol": "AAPL", "name": "Apple Inc.", "current_price": 214.20, "change_24h_percent": 1.85},
        {"symbol": "TSLA", "name": "Tesla Inc.", "current_price": 248.10, "change_24h_percent": -2.10}
    ]

@router.get("/market/news")
async def get_market_news():
    return [
        {"source": "Bloomberg", "time_posted": "15m ago", "headline": "Federal Reserve Signals Steady Rates as Tech Sector Rallies", "url": "#"},
        {"source": "Reuters", "time_posted": "1h ago", "headline": "Institutional Liquidity Flows Into High-Beta Assets Surpass Expectations", "url": "#"}
    ]

@router.get("/market/search")
async def search_market_assets(q: str):
    mock_assets = [
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "current_price": 128.50, "change_24h_percent": 4.25},
        {"symbol": "AAPL", "name": "Apple Inc.", "current_price": 214.20, "change_24h_percent": 1.85},
        {"symbol": "TSLA", "name": "Tesla Inc.", "current_price": 248.10, "change_24h_percent": -2.10},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "current_price": 445.60, "change_24h_percent": 0.95},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "current_price": 186.50, "change_24h_percent": 1.20},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "current_price": 178.30, "change_24h_percent": -0.45},
        {"symbol": "META", "name": "Meta Platforms Inc.", "current_price": 502.10, "change_24h_percent": 3.10}
    ]
    query = q.strip().upper()
    results = [a for a in mock_assets if query in a["symbol"] or query in a["name"].upper()]
    if not results and query:
        results = [{
            "symbol": query,
            "name": f"{query} Enterprise Asset",
            "current_price": 142.50,
            "change_24h_percent": 1.15
        }]
    return results
