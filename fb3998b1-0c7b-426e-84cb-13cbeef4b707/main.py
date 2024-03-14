from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Identify the assets of interest
        self.tickers = ["AAPL", "MSFT", "GOOGL"]  # Example tickers; consider stable, blue-chip companies
    
    @property
    def assets(self):
        """List of assets the strategy will operate on."""
        return self.tickers

    @property
    def interval(self):
        """Data interval for analysis. Using '1day' for long-term investing."""
        return "1day"

    def run(self, data):
        allocation_dict = {ticker: 0 for ticker in self.tickers}  # Initialize all allocations to 0
        for ticker in self.tickers:
            # Compute the MACD and its signal line for each ticker
            macd_data = MACD(ticker=ticker, data=data["ohlcv"], fast=12, slow=26)
            if macd_data is None:
                continue  # Skip if MACD data is unavailable
            macd_line = macd_data["MACD"]
            signal_line = macd_data["signal"]
            
            if len(macd_line) < 1 or len(signal_line) < 1:
                continue  # Ensure there's enough data
            
            # Check if the MACD line crossed above the signal line (buy signal)
            if macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
                allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equally distribute allocation among tickers
            # Note: Exit logic can be added here if required, based on your risk tolerance
            
        # Log the allocation for review
        log("Target allocation: " + str(allocation_dict))
        return TargetAllocation(allocation_dict)