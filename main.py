from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==========================================
# 1. IMPORTS FROM OUR SRC FOLDER
# ==========================================
from src.database import engine, init_db
from src import models
from src.api import router as api_router

# ==========================================
# 2. DATABASE INITIALIZATION & SEEDING
# ==========================================
# Creates the physical tables in SQLite
models.Base.metadata.create_all(bind=engine)

# Seeds initial default data (User & Wallet)
init_db()

# ==========================================
# 3. FASTAPI APP CREATION
# ==========================================
app = FastAPI(
    title="Tridding Engine API",
    description="Core backend for the Tridding financial platform",
    version="1.0.0"
)

# ==========================================
# 4. CORS CONFIGURATION (Security)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 5. ROUTER REGISTRATION
# ==========================================
app.include_router(api_router)

# ==========================================
# 6. ROOT HEALTH CHECK
# ==========================================
@app.get("/", tags=["Health"])
async def root():
    """Simple endpoint to verify the engine is running."""
    return {"status": "online", "message": "Tridding Engine is fully operational."}