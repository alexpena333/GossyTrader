# Tridding: Gamified EdFintech Ecosystem (Architectural Concept)

Tridding is an educational financial technology (EdFintech) platform designed to gamify financial literacy, simulate market mechanics, and safely extract anonymized behavioral data for market insights. This repository serves as the **V1 Architectural Scaffolding** for the ecosystem.

## Core Vision & Architecture
The platform is built to operate strictly on simulated currency and live market data (e.g., Yahoo Finance), ensuring a risk-free environment. The backend is compartmentalized into three operational pillars, monitored by a conversational AI engine.

### 1. The Game Pillars
*   **FUT:** A long-term investment simulator focused on smart-holding strategies and portfolio management.
*   **NOW:** A high-frequency trading terminal for intraday practice, stress-testing decision-making under low latency.
*   **IF:** A binary prediction market utilizing bookmaker-style overround logic to teach probability and market sentiment.

### 2. The AI & Data Engine
*   **Conversational AI:** An integrated chat interface that analyzes real-time financial news and educates the user on market trends.
*   **Invisible Profiling:** The AI engine silently builds an investor profile based on the user's trades, reactions, and risk tolerance.
*   **Privacy & Monetization:** Engineered with strict GDPR/CCPA compliance, the system aggregates anonymized behavioral data to generate B2B marketing insights and scalable enterprise licensing for educational institutions.

## Technical Structure
*   `src/ai/`: Contains the logic for the Master Agent, transformer models, and Reinforcement Learning environments.
*   `src/core/`: Manages the virtual ledger, database connections, and privacy compliance algorithms.
*   `src/dashboard/`: The entry point for the user interface and terminal metrics.
*   `tridding-web/`: The Next.js frontend architecture.

*Disclaimer: This project is strictly educational. It does not provide financial advice, handle real money, or promise wealth. It promises knowledge.*
