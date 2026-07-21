from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
import random
from typing import List

# ==========================================
# 1. DATA MODELS (SCHEMAS)
# ==========================================

class Future33OrderRequest(BaseModel):
    """Data payload required from the frontend to place a Future33 order."""
    user_id: str
    asset_symbol: str
    amount: float
    target_price: float
    expiration_date: datetime

class Future33OrderResponse(BaseModel):
    """Response payload sent back to the frontend after processing."""
    order_id: str
    status: str
    frozen_amount: float
    message: str

class AssetDTO(BaseModel):
    """Data Transfer Object for Market Assets."""
    symbol: str
    name: str
    current_price: float
    change_24h_percent: float
    is_trending: bool

class ChartDataPoint(BaseModel):
    """Represents a single point in the performance chart (User vs S&P500)."""
    timestamp: str
    portfolio_value: float
    sp500_value: float

class DashboardSummaryResponse(BaseModel):
    """
    Complete payload to power the iOS/Web home screen.
    Includes the red/green indicators and chart history.
    """
    total_balance: float
    available_buying_power: float
    total_profit_loss: float
    profit_loss_percentage: float
    is_positive: bool  
    chart_data: List[ChartDataPoint]

class NewsDTO(BaseModel):
    """Schema for market news articles."""
    headline: str
    source: str
    time_posted: str
    url: str

# ==========================================
# 2. MOCK DATABASE & MARKET DATA
# ==========================================

MOCK_WALLET_BALANCES = {"user_123": 10000.00}
MOCK_ESCROW_BALANCES = {"user_123": 0.00}

MOCK_MARKET = [
    AssetDTO(symbol="AAPL", name="Apple Inc.", current_price=185.30, change_24h_percent=1.2, is_trending=True),
    AssetDTO(symbol="NVDA", name="NVIDIA Corp.", current_price=480.15, change_24h_percent=4.5, is_trending=True),
    AssetDTO(symbol="SPY", name="S&P 500 ETF", current_price=445.10, change_24h_percent=-0.3, is_trending=False),
    AssetDTO(symbol="TSLA", name="Tesla Inc.", current_price=240.50, change_24h_percent=-2.1, is_trending=False),
    AssetDTO(symbol="CRWD", name="CrowdStrike", current_price=160.20, change_24h_percent=8.4, is_trending=True)
]

MOCK_NEWS = [
    NewsDTO(headline="Tech stocks surge as AI demand hits all-time highs", source="Financial Times", time_posted="2 hours ago", url="https://tridding.com/news/1"),
    NewsDTO(headline="Federal Reserve indicates potential rate cuts for Q4", source="Wall Street Journal", time_posted="4 hours ago", url="https://tridding.com/news/2"),
    NewsDTO(headline="New regulations affect crypto and biotech sectors", source="Bloomberg", time_posted="5 hours ago", url="https://tridding.com/news/3")
]

# ==========================================
# 3. CORE BUSINESS LOGIC: TRADING & ESCROW
# ==========================================

def place_future33_order(order: Future33OrderRequest) -> Future33OrderResponse:
    """Validates user balance, moves funds to escrow, and registers a PENDING Future33 order."""
    current_available = MOCK_WALLET_BALANCES.get(order.user_id, 0.0)
    
    if current_available < order.amount:
        raise ValueError("Insufficient funds. Please deposit more capital.")
        
    # Execute Escrow Transfer
    MOCK_WALLET_BALANCES[order.user_id] -= order.amount
    MOCK_ESCROW_BALANCES[order.user_id] = MOCK_ESCROW_BALANCES.get(order.user_id, 0.0) + order.amount
    
    order_id = f"F33-{uuid.uuid4().hex[:8].upper()}"
    
    return Future33OrderResponse(
        order_id=order_id,
        status="PENDING",
        frozen_amount=order.amount,
        message=f"Success: ${order.amount} frozen in escrow for {order.asset_symbol}."
    )

# ==========================================
# 4. CORE BUSINESS LOGIC: DASHBOARD & MARKET
# ==========================================

def get_trending_assets() -> List[AssetDTO]:
    """Returns top moving assets for the explore page."""
    trending = [asset for asset in MOCK_MARKET if asset.is_trending]
    return sorted(trending, key=lambda x: x.change_24h_percent, reverse=True)

def get_top_losers() -> List[AssetDTO]:
    """Returns assets with the biggest negative change for the 'Top Losers' section."""
    losers = [asset for asset in MOCK_MARKET if asset.change_24h_percent < 0]
    return sorted(losers, key=lambda x: x.change_24h_percent)

def search_market_assets(query: str) -> List[AssetDTO]:
    """Search engine for assets by symbol or company name."""
    query_lower = query.lower()
    return [
        asset for asset in MOCK_MARKET 
        if query_lower in asset.symbol.lower() or query_lower in asset.name.lower()
    ]

def get_market_news() -> List[NewsDTO]:
    """Returns the latest market news feed."""
    return MOCK_NEWS

def get_user_dashboard(user_id: str) -> DashboardSummaryResponse:
    """Compiles financial data, calculates P&L, and generates chart data."""
    available = MOCK_WALLET_BALANCES.get(user_id, 0.0)
    frozen = MOCK_ESCROW_BALANCES.get(user_id, 0.0)
    total = available + frozen
    
    initial_investment = 9500.00 
    total_pl = total - initial_investment
    pl_percentage = (total_pl / initial_investment) * 100

    chart = []
    base_time = datetime.now() - timedelta(days=7)
    for i in range(7):
        time_point = base_time + timedelta(days=i)
        chart.append(ChartDataPoint(
            timestamp=time_point.strftime("%Y-%m-%d"),
            portfolio_value=initial_investment + random.uniform(-100, 200) + (i * 50),
            sp500_value=initial_investment + random.uniform(-50, 100) + (i * 20)
        ))

    return DashboardSummaryResponse(
        total_balance=total,
        available_buying_power=available,
        total_profit_loss=round(total_pl, 2),
        profit_loss_percentage=round(pl_percentage, 2),
        is_positive=total_pl >= 0,
        chart_data=chart
    )