'''
This module calculates the fees for buying and selling cryptocurrencies on different exchanges.
Fees included are trading fees, spread fees, payment fees, network fees, blockchain fees, and withdrawal fees.
It allows us to calculate the total fees for a given transaction along with the price arbitrage between the biggest spread.
'''

from exchange_fee_structure_data import fee_structures

class FeeCalculator:
    """Calculator for cryptocurrency_withdrawal exchange fees"""
    FEE_STRUCTURES = fee_structures

    def __init__(self, exchange_buy, exchange_sell, crypto, crypto_amount, crypto_price_buy, crypto_price_sell, currency_withdrawal, exchange_rates):
        self.exchange_buy = exchange_buy.lower()  # Convert to lowercase
        self.exchange_sell = exchange_sell.lower()  # Convert to lowercase
        self.crypto = crypto
        self.crypto_amount = crypto_amount
        self.crypto_price_buy = crypto_price_buy
        self.crypto_price_sell = crypto_price_sell
        self.currency_withdrawal = currency_withdrawal
        self.exchange_rates = exchange_rates

    def get_trading_fees(self, exchange, operation):
        """Get trading fees for an exchange"""
        return self.FEE_STRUCTURES[exchange.lower()][f"trading_fee_{operation}"]

    def get_spread_fees(self, exchange, operation):
        """Get spread fees for an exchange"""
        return self.FEE_STRUCTURES[exchange.lower()][f"spread_fee_{operation}"]

    def get_withdrawal_fee(self, exchange, currency_withdrawal, withdrawal_type):
        """Get withdrawal fee based on currency_withdrawal type"""
        fees = self.FEE_STRUCTURES[exchange.lower()]["withdrawal_fee"]
        if withdrawal_type == "crypto":
            return fees["crypto"].get(currency_withdrawal, 0.0)
        
        # For fiat, get the first available withdrawal method for the currency
        fiat_methods = fees["fiat"][currency_withdrawal]
        withdrawal_method = next(iter(fiat_methods))  # Get the first method
        fiat_fee = fiat_methods[withdrawal_method]

        # Handle both dictionary with 'rate' key and direct float value formats
        rate = self.exchange_rates[currency_withdrawal]
        if isinstance(rate, dict) and 'rate' in rate:
            rate = rate['rate']
        
        # Ensure rate is a float
        if not isinstance(rate, (int, float)):
            print(f"Invalid rate for {currency_withdrawal}: {rate}")
            raise ValueError(f"Rate for {currency_withdrawal} is not a valid number")


        # Normalize the fiat fee to USD using the exchange rate
        return fiat_fee * rate

    def calculate_fees(self):
        """Calculate total fees for buying and selling crypto"""
        

        # Calculate buying fees
        trading_fee_buy = self.crypto_amount * self.crypto_price_buy * self.get_trading_fees(self.exchange_buy, "buy")
        

        # spread_fee_buy = self.crypto_amount * self.crypto_price_buy * self.get_spread_fees(self.exchange_buy, "buy")
        payment_fee = self.crypto_amount * self.crypto_price_buy * self.FEE_STRUCTURES[self.exchange_buy]["payment_fee"]
        

        # Calculate selling fees
        trading_fee_sell = self.crypto_amount * self.crypto_price_sell * self.get_trading_fees(self.exchange_sell, "sell")
        

        # spread_fee_sell = self.crypto_amount * self.crypto_price_sell * self.get_spread_fees(self.exchange_sell, "sell")

        # Calculate withdrawal fee
        withdrawal_type = "crypto" if self.currency_withdrawal.upper() == self.crypto.upper() else "fiat"
        withdrawal_fee = self.get_withdrawal_fee(self.exchange_sell, self.currency_withdrawal, withdrawal_type)
        

        total_fees = (
            trading_fee_buy +
            # spread_fee_buy +
            # payment_fee +
            trading_fee_sell +
            # spread_fee_sell +
            withdrawal_fee
        )
        # Commented out print that slows down processing
        # print(f"Total Fees: {total_fees}")

        return {
            "trading_fee_buy": trading_fee_buy,
            # "spread_fee_buy": spread_fee_buy,
            "payment_fee": payment_fee,
            "trading_fee_sell": trading_fee_sell,
            # "spread_fee_sell": spread_fee_sell,
            "withdrawal_fee": withdrawal_fee,
            "total_fees": total_fees,
            "price_arbitrage": self.crypto_price_sell - self.crypto_price_buy,
            "arbitrage_after_fees": self.crypto_price_sell - self.crypto_price_buy - total_fees
        }
    
    def display_fees(self):
        """Calculate and display the total accumulated fees"""
        fees = self.calculate_fees()
        print("Fee Breakdown:")
        for key, value in fees.items():
            print(f"{key}: ${value:.2f}")


if __name__ == "__main__":
    EXAMPLE_TIMESTAMP = '2023-10-01T00:00:00Z'
    exchange_rates = {
        'USD': {'rate': 1.0, 'timestamp': EXAMPLE_TIMESTAMP},
        'EUR': {'rate': 1.1, 'timestamp': EXAMPLE_TIMESTAMP},  # 1 EUR = 1.1 USD
        'GBP': {'rate': 1.3, 'timestamp': EXAMPLE_TIMESTAMP}   # 1 GBP = 1.3 USD
    }
    # Example usage
    fee_calculator = FeeCalculator(
        exchange_buy="coinbase",
        exchange_sell="binance",
        crypto="BTC",
        crypto_amount=1,
        crypto_price_buy=102124.60,
        crypto_price_sell=102189.78,
        currency_withdrawal="USD",
        exchange_rates=exchange_rates
    )

    fee_calculator.display_fees()

__all__ = ['FeeCalculator']
