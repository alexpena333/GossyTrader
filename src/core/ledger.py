import sqlite3
from decimal import Decimal
from datetime import datetime
from src.core.database import get_db_connection

def create_user(username: str, email: str, password_hash: str):
    """Registers a new user and provisions default trading accounts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, datetime.utcnow().isoformat())
        )
        user_id = cursor.lastrowid
        
        for mode in ['paper', 'live', 'if33']:
            cursor.execute(
                "INSERT INTO accounts (user_id, mode, balance, currency, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, mode, '0.00', 'USD', datetime.utcnow().isoformat())
            )
        conn.commit()
        return {"status": "success", "user_id": user_id, "username": username}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def authenticate_user(email: str, password_hash: str):
    """Authenticates a user against stored credentials."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE email = ? AND password_hash = ?", (email, password_hash))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise ValueError("Invalid email or password")
    return {"id": user["id"], "username": user["username"], "email": user["email"]}

def get_account_id(user_id: int, mode: str) -> int:
    """Retrieves account ID for a given user and trading mode."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM accounts WHERE user_id = ? AND mode = ?", (user_id, mode))
    acc = cursor.fetchone()
    conn.close()
    if not acc:
        raise ValueError(f"Account not found for user {user_id} in mode {mode}")
    return acc["id"]

def deposit_cash(account_id: int, amount: Decimal):
    """Deposits cash into a specific account."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    acc = cursor.fetchone()
    if not acc:
        conn.close()
        raise ValueError("Account not found")
    
    new_balance = Decimal(acc["balance"]) + amount
    cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (str(new_balance), account_id))
    conn.commit()
    conn.close()
    return {"status": "success", "new_balance": str(new_balance)}

def setup_auto_deposit(account_id: int, amount: Decimal, frequency: str, start_date: str):
    """Sets up an automated deposit schedule."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO auto_deposits (account_id, amount, frequency, start_date, status, created_at) VALUES (?, ?, ?, ?, 'active', ?)",
        (account_id, str(amount), frequency, start_date, datetime.utcnow().isoformat())
    )
    conn.commit()
    deposit_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "auto_deposit_id": deposit_id}

def process_pending_auto_deposits():
    """Processes active automated deposits."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, account_id, amount FROM auto_deposits WHERE status = 'active'")
    deposits = cursor.fetchall()
    
    for dep in deposits:
        deposit_cash(dep["account_id"], Decimal(dep["amount"]))
        
    conn.close()
    return True
