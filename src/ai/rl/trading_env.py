class TradingEnv:
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = 0  # 0: None, 1: Long
        print(f"Trading Environment initialized with balance: ${initial_balance}")

    def reset(self):
        self.balance = self.initial_balance
        self.position = 0
        return self.balance

    def step(self, action: str, current_price: float):
        """
        Executes an action ('BUY', 'SELL', 'HOLD') within the simulation environment.
        """
        reward = 0.0
        if action.upper() == "BUY" and self.position == 0:
            self.position = 1
            reward = 0.1  # Simulated incremental reward
        elif action.upper() == "SELL" and self.position == 1:
            self.position = 0
            reward = 0.5  # Simulated realization reward

        return self.balance, reward, False