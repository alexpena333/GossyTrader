from decimal import Decimal

def create_if33_market(symbol: str, expiry: str):
    """Creates a new IF33 binary market."""
    return {"status": "market_created", "symbol": symbol, "expiry": expiry}

def place_if33_bet(user_id: int, market_id: int, chosen_option: str, amount: Decimal):
    """Registers a prediction in the IF33 market."""
    return {
        "status": "bet_placed", 
        "user_id": user_id, 
        "market_id": market_id, 
        "option": chosen_option, 
        "amount": str(amount)
    }
