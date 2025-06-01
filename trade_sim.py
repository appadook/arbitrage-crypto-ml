from fee_calc import FeeCalculator

class TradeSimulator:
    """
    A simple trade simulator for backtesting crypto-arbitrage strategies and seeing how much profit/loss they would make 
    """
    
    def parse_strategy(self, strategy):
        """
        Parse a strategy string in the format 'BUY@EXCHANGE1->SELL@EXCHANGE2'
        and extract the buy and sell exchanges.
        
        Args:
            strategy (str): Strategy string in the format 'BUY@EXCHANGE1->SELL@EXCHANGE2'
            
        Returns:
            tuple: (buy_exchange, sell_exchange) - names of the exchanges
            
        Example:
            >>> simulator = TradeSimulator()
            >>> simulator.parse_strategy('BUY@BINANCE->SELL@BITSTAMP')
            ('BINANCE', 'BITSTAMP')
        """
        if strategy == 'No profitable arbitrage':
            return (None, None)
        try:
            # Split the strategy string by the arrow
            parts = strategy.split('->')
            if len(parts) != 2:
                raise ValueError(f"Invalid strategy format: {strategy}. Expected 'BUY@EXCHANGE1->SELL@EXCHANGE2'")
            
            # Extract the buy exchange
            buy_part = parts[0].strip()
            if not buy_part.startswith('BUY@'):
                raise ValueError(f"Invalid buy part: {buy_part}. Expected 'BUY@EXCHANGE'")
            buy_exchange = buy_part[4:]  # Remove 'BUY@' prefix
            
            # Extract the sell exchange
            sell_part = parts[1].strip()
            if not sell_part.startswith('SELL@'):
                raise ValueError(f"Invalid sell part: {sell_part}. Expected 'SELL@EXCHANGE'")
            sell_exchange = sell_part[5:]  # Remove 'SELL@' prefix
            
            return (buy_exchange, sell_exchange)
        except Exception as e:
            raise ValueError(f"Failed to parse strategy '{strategy}': {str(e)}")
    
    def simulate(self, strategy, buy_price=None, sell_price=None):
        """
        Simulate trades using the provided strategy.
        
        Args:
            strategy (str): Strategy string in the format 'BUY@EXCHANGE1->SELL@EXCHANGE2'
            
        Returns:
            dict: Results of the simulation including profit/loss
        """
        # Parse the strategy to get buy and sell exchanges
        buy_exchange, sell_exchange = self.parse_strategy(strategy)

        if buy_exchange is None or sell_exchange is None:
            return 0
        
        crypto = "BTC"  # Assuming BTC for simplicity
        crypto_amount = 1.0  # Standard amount for simulation
        currency_withdrawal = "USD"  # Assuming USD for withdrawal
        exchange_rates = {"USD": 1.0}  # Assuming USD for simplicity
        fee_calculator = FeeCalculator(buy_exchange, sell_exchange, crypto, crypto_amount, buy_price, sell_price, currency_withdrawal, exchange_rates)
        
        results = fee_calculator.calculate_fees()
        arbitrage = results['arbitrage_after_fees'] 

        return arbitrage
    
# Example usage
if __name__ == "__main__":
    # Create a simulator instance
    simulator = TradeSimulator()
    
    # Example strategy string in the format 'BUY@EXCHANGE1->SELL@EXCHANGE2'
    strategy = "BUY@BINANCE->SELL@BITSTAMP"
    
    # Parse the strategy to extract exchanges
    try:
        buy_exchange, sell_exchange = simulator.parse_strategy(strategy)
        print(f"Strategy: {strategy}")
        print(f"Buy Exchange: {buy_exchange}")
        print(f"Sell Exchange: {sell_exchange}")
    except ValueError as e:
        print(f"Error parsing strategy: {e}")
    
    # Run a simulation with the strategy
    try:
        results = simulator.simulate(strategy, buy_price=30000, sell_price=31000)
        print("\nSimulation Results:")
        print(f"Arbitrage after fees: ${results:.2f}")
        if results > 0:
            print("This strategy is profitable!")
        else:
            print("This strategy is not profitable.")
    except Exception as e:
        print(f"Error during simulation: {e}")
    
    # # Additional examples with different exchanges
    # print("\nAdditional Examples:")
    # example_strategies = [
    #     "BUY@KRAKEN->SELL@COINBASE",
    #     "BUY@GEMINI->SELL@BITFINEX",
    #     "BUY@KUCOIN->SELL@HUOBI"
    # ]
    
    # for strat in example_strategies:
    #     try:
    #         buy_ex, sell_ex = simulator.parse_strategy(strat)
    #         print(f"Strategy: {strat} => Buy: {buy_ex}, Sell: {sell_ex}")
    #     except ValueError as e:
    #         print(f"Error parsing {strat}: {e}")





