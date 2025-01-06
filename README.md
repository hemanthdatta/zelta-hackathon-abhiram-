# BTC/USDT Trading Strategy

This repository contains an algorithmic trading strategy for the BTC/USDT cryptocurrency market. The strategy uses a combination of technical indicators including EMA crossovers and RSI for trade signals, with dynamic position sizing and risk management.

## Features

- EMA crossover strategy with RSI confirmation
- Dynamic position sizing based on ATR
- Risk management with stop losses
- Comprehensive performance metrics
- Backtesting framework integration

## Performance Metrics

- Net Profit: 126.58%
- Total Closed Trades: 11
- Win Rate: 9.09%
- Max Drawdown: -74.01%
- Average Trade: 8.09%
- Sharpe Ratio: 0.31
- Sortino Ratio: 0.60

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download BTC/USDT data and place it in the `data` directory

3. Run the strategy:
```bash
python trading_strategy.py
```

## Project Structure

- `trading_strategy.py`: Main strategy implementation
- `data_downloader.py`: Utility for data preparation
- `requirements.txt`: Project dependencies
- `data/`: Directory containing OHLCV data

## Data

The strategy uses 1-hour OHLCV data for BTC/USDT from 2019 to 2023. Data should be placed in the `data` directory.

## Risk Warning

Cryptocurrency trading involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results.
