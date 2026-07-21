class DashboardApp:
    def __init__(self):
        print("Tridding Dashboard interface initialized.")

    def render_status(self, engine_status: str, balance: float):
        """
        Renders current metrics for the engine interface.
        """
        print("--- TRIDDING SYSTEM DASHBOARD ---")
        print(f"Status: {engine_status}")
        print(f"Current Balance: ${balance:,.2f}")
        print("---------------------------------")

if __name__ == "__main__":
    dash = DashboardApp()
    dash.render_status("ONLINE", 10000.0)
