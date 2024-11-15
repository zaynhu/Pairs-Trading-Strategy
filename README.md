# Pairs Trading Project

This project implements a statistical arbitrage strategy known as pairs trading, leveraging cointegration between two assets to capture profit from mean-reverting behavior.

## Purpose

The goal of this project is to use statistical tests to identify pairs of stocks with a cointegrated relationship. The strategy takes long and short positions in these pairs, profiting from price deviations that revert to the mean over time.

## Approach

1. **Cointegration Analysis**: Identifying pairs of stocks with a high degree of cointegration, which suggests a stable long-term relationship and provides the basis for mean-reversion trading.
2. **Mean Reversion Strategy**: Using a moving average and z-score threshold to enter long or short positions when the price ratio between the two assets deviates significantly from its historical mean.

## Method

1. **Data Collection and Cointegration Test**:
   - Using historical price data for a set of stocks to identify cointegrated pairs. The Engle-Granger two-step method and ADF tests are applied to confirm cointegration.
   
2. **Spread and Z-Score Calculation**:
   - For cointegrated pairs, calculate the price spread and z-score between two stocks, e.g., HPQ and ORCL.
   - If the z-score of the price ratio crosses predefined thresholds, this generates buy or sell signals.
   
3. **Trading Model Implementation**:
   - Develop and test the pairs trading strategy in QuantConnect using a threshold for z-scores to determine when to enter or exit positions.
   - The strategy dynamically rebalances based on changes in the spread between paired stocks.

## Result

This pairs trading algorithm achieves returns by exploiting the mean-reverting relationship between cointegrated stock pairs. For example, during backtesting, the strategy successfully identified trading signals for HPQ and ORCL, generating long/short positions that capitalized on the price divergence and convergence.

---

### Dependencies

- Python libraries: `numpy`, `pandas`, `statsmodels`, `matplotlib`, `seaborn`, `yfinance`
- QuantConnect platform for live and backtesting
