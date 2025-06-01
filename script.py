from fee_calc import FeeCalculator
import pandas as pd

def get_min_max_prices_row(row, columns):
    """
    Given a row (Series) and a list of columns, return the lowest price, highest price,
    and their respective column names (exchange only, without '_USD').

    Returns:
        min_price (float): The lowest price value.
        min_col (str): The exchange name with the lowest price.
        max_price (float): The highest price value.
        max_col (str): The exchange name with the highest price.
    """
    prices = row[columns]
    min_col = prices.idxmin()
    min_price = prices[min_col]
    max_col = prices.idxmax()
    max_price = prices[max_col]
    # Only keep the exchange name before '_USD'
    min_col_short = min_col.split('_USD')[0]
    max_col_short = max_col.split('_USD')[0]
    return {
        "min_price": min_price,
        "min_col": min_col_short,
        "max_price": max_price,
        "max_col": max_col_short
    }

def calculate_arbitrage(row):
    """
    Calculate arbitrage opportunity and fees for a given row of data
    
    Args:
        row: DataFrame row containing price data for different exchanges
    
    Returns:
        Dictionary with arbitrage details: strategy, arbitrage percentage, total fees, 
        and arbitrage after fees
    """
    # Get USD price columns
    usd_columns = [col for col in row.index if col.endswith('_USD')]
    
    # Get min and max prices
    price_info = get_min_max_prices_row(row, usd_columns)
    
    # Extract values
    min_price = price_info["min_price"]
    min_exchange = price_info["min_col"]
    max_price = price_info["max_price"]
    max_exchange = price_info["max_col"]
    
    # Calculate raw arbitrage (before fees)
    raw_arbitrage = max_price - min_price
    arbitrage_pct = (raw_arbitrage / min_price) * 100
    
    
    # Initialize fee calculator
    # Using 1 BTC as standard amount for calculation
    crypto_amount = 1.0
    
    fee_calc = FeeCalculator(
        exchange_buy=min_exchange,
        exchange_sell=max_exchange,
        crypto="BTC",
        crypto_amount=crypto_amount,
        crypto_price_buy=min_price,
        crypto_price_sell=max_price,
        currency_withdrawal="USD",
        exchange_rates={"USD": 1.0}  # Not needed for USD-only calculations
    )
    
    # Calculate fees
    fees = fee_calc.calculate_fees()
    
    # Construct strategy string: BUY@exchange1->SELL@exchange2
    strategy = f"BUY@{min_exchange}->SELL@{max_exchange}"


    # strategy_detailed = f"BUY@{min_exchange} FOR ({min_price}) -> SELL@{max_exchange} FOR ({max_price})"
    
    return {
        # "strategy_detailed": strategy_detailed if fees["arbitrage_after_fees"] > 0 else "No profitable arbitrage",
        "strategy": strategy if fees["arbitrage_after_fees"] > 0 else "No profitable arbitrage",
        "arbitrage(%)": arbitrage_pct,
        "total_fees": fees["total_fees"],
        "arbitrage_after_fees": fees["arbitrage_after_fees"]
    }


df = pd.read_csv("cleaned_crypto_arbitrage_intermediate.csv")  

# Total row count for progress tracking
total_rows = len(df)
print(f"Processing {total_rows} rows...")

# Create a function to process rows with progress tracking
def process_with_progress(dataframe):
    results = []
    for i, row in dataframe.iterrows():
        result = calculate_arbitrage(row)
        results.append(result)
        # Print progress every 1000 rows
        if i % 1000 == 0:
            print(f"Processed {i}/{total_rows} rows ({i/total_rows:.1%})")
    return pd.DataFrame(results)

# Compute arbitrage and fees for each row with progress tracking
arbitrage_df = process_with_progress(df)

# Append the new columns to the original DataFrame
df = pd.concat([df, arbitrage_df], axis=1)

# Save the enriched DataFrame to CSV
print("Saving results to CSV...")
df.to_csv("cleaned_crypto_arbitrage_with_fees.csv", index=False)
print("Processing complete!")