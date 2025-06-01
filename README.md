# Cryptocurrency Arbitrage Prediction

## Overview
This project investigates the use of machine learning and data mining techniques to predict arbitrage opportunities in cryptocurrency markets. Using data collected through CoinAPI & XChangeAPI websockets, this research is part of a senior thesis project in Economics on "Arbitrage in the cryptocurrency market".

## Dataset
- **Content:** Price data for Bitcoin across multiple exchanges (Coinbase, Binance, Kraken, Bitstamp) in USD
- **Collection Period:** May 22-26, 2025 (5-day period)
- **Scale:** 28,006,444 instances with 17 raw features + 4 transformation features
- **Collection Method:** Real-time websocket data

## Research Goals
- Classify the most profitable arbitrage strategy route based on current market conditions
- Predict whether the next timestamp will present a profitable arbitrage opportunity
- Identify if price points in specific markets are diverging from or converging to cross-market means
- Evaluate how vulnerable arbitrage opportunities are to latency risks

## Project Structure
- **ML Project crypto-arbitrage.ipynb**: Main Jupyter notebook containing data analysis and ML models
- **fee_calc.py**: Module for calculating exchange fees for cryptocurrency trading
- **exchange_fee_structure_data.py**: Contains fee structures for various exchanges
- **trade_sim.py**: Simulator for backtesting crypto-arbitrage strategies
- **script.py**: Utility scripts for data processing
- **data/**: Directory containing raw CSV data files

## Methodology

### Data Preprocessing
1. Loading and consolidating data from five separate CSV files
2. Filtering to Bitcoin-only data
3. Handling missing values and timestamp deduplication
4. Feature engineering (price volatility, change percentages, time-based features)
5. Creating target variables for next-timestamp arbitrage strategy

### Arbitrage Calculation
- Identifies exchanges with lowest and highest prices
- Calculates raw arbitrage opportunity (percentage difference)
- Accounts for all applicable exchange fees using the FeeCalculator
- Determines if arbitrage is profitable after fees
- Creates a strategy string in the format `BUY@EXCHANGE1->SELL@EXCHANGE2`

### Machine Learning Models
The project evaluates several classification models to predict the optimal arbitrage strategy:
1. **Baseline Models**:
   - DummyClassifier (most frequent strategy)
   - DummyClassifier (prior probability strategy)

2. **Advanced Models**:
   - Random Forest Classifier
   - Support Vector Machine (SVM with RBF kernel)
   - Logistic Regression
   - Gradient Boosting Classifier
   - Neural Network (MLPClassifier) - commented out in the final version

3. **Evaluation Method**:
   - TimeSeriesSplit cross-validation (respecting temporal order of data)
   - Trading simulation to evaluate real-world profitability
   - Metrics: accuracy, total profit, trade success rate, average profit per trade

## Results
The models were evaluated not just on prediction accuracy but on actual simulated trading profitability. Random Forest performed exceptionally well, achieving:
- Mean Accuracy: 86.04%
- Total Simulated Profit: $897,381.45
- Trade Success Rate: 99.87%
- Average Profit per Trade: $29.76

## Usage
1. Clone this repository
2. Install required dependencies: pandas, numpy, scikit-learn, matplotlib, seaborn
3. Run the Jupyter notebook to see all analysis and results

## Dependencies
- Python 3.12
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- missingno
- jupyter

## License
This project is part of academic research at Union College and all rights are reserved.

## Author
Kurtik Appadoo


