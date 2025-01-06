import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
import ta
from datetime import datetime

class BTCTradingStrategy(Strategy):
    # Strategy parameters
    n1 = 20  # Fast EMA period
    n2 = 50  # Slow EMA period
    rsi_period = 14
    rsi_overbought = 70
    rsi_oversold = 30
    
    def init(self):
        # Calculate indicators
        # EMA
        self.ema1 = self.I(ta.trend.ema_indicator, pd.Series(self.data.Close), self.n1)
        self.ema2 = self.I(ta.trend.ema_indicator, pd.Series(self.data.Close), self.n2)
        
        # RSI
        self.rsi = self.I(ta.momentum.rsi, pd.Series(self.data.Close), self.rsi_period)
        
        # Volatility - ATR
        self.atr = self.I(ta.volatility.average_true_range, 
                         pd.Series(self.data.High), 
                         pd.Series(self.data.Low), 
                         pd.Series(self.data.Close), 
                         window=14)

    def next(self):
        # Risk management - Position sizing
        risk_per_trade = 0.02  # 2% risk per trade
        
        # Entry conditions
        if not self.position:  # If not in position
            # Bullish conditions
            if (self.ema1[-1] > self.ema2[-1] and  # Fast EMA above slow EMA
                self.rsi[-1] < self.rsi_oversold):  # RSI oversold
                
                # Calculate position size based on ATR
                stop_distance = self.atr[-1] * 2
                entry_price = self.data.Close[-1]
                stop_price = entry_price - stop_distance
                
                # Calculate position size based on risk
                risk_amount = self.equity * risk_per_trade
                position_size = risk_amount / (entry_price - stop_price)
                
                # Round position size to whole number
                position_size = max(1, round(position_size))
                
                # Enter long position
                self.buy(size=position_size, sl=stop_price)
                
            # Bearish conditions
            elif (self.ema1[-1] < self.ema2[-1] and  # Fast EMA below slow EMA
                  self.rsi[-1] > self.rsi_overbought):  # RSI overbought
                
                # Calculate position size based on ATR
                stop_distance = self.atr[-1] * 2
                entry_price = self.data.Close[-1]
                stop_price = entry_price + stop_distance
                
                # Calculate position size based on risk
                risk_amount = self.equity * risk_per_trade
                position_size = risk_amount / (stop_price - entry_price)
                
                # Round position size to whole number
                position_size = max(1, round(position_size))
                
                # Enter short position
                self.sell(size=position_size, sl=stop_price)

def load_and_prepare_data(file_path):
    # Load data
    df = pd.read_csv(file_path)
    
    # Convert datetime to proper format
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    
    # Ensure OHLCV columns are present and properly named
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    df.columns = [col.lower() for col in df.columns]
    
    # Rename columns to match Backtest requirements
    column_mapping = {
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # Remove any missing values
    df.dropna(inplace=True)
    
    return df

def run_backtest(data):
    # Initialize and run backtest
    bt = Backtest(data, BTCTradingStrategy,
                 cash=100000,  # Initial capital
                 commission=.002,  # Commission rate
                 exclusive_orders=True)
    
    # Run optimization
    stats = bt.run()
    
    return stats, bt

def print_metrics(stats):
    metrics = {
        'Net Profit (%)': stats['Return [%]'],
        'Total Closed Trades': stats['# Trades'],
        'Win Rate (%)': stats['Win Rate [%]'],
        'Max Drawdown (%)': stats['Max. Drawdown [%]'],
        'Average Trade (%)': stats['Avg. Trade [%]'],
        'Sharpe Ratio': stats['Sharpe Ratio'],
        'Sortino Ratio': stats['Sortino Ratio'],
        'Buy & Hold Return (%)': stats['Buy & Hold Return [%]'],
        'Max Trade Duration': stats['Max. Trade Duration'],
        'Avg Trade Duration': stats['Avg. Trade Duration'],
    }
    
    print("\nStrategy Performance Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}" if isinstance(value, float) else f"{metric}: {value}")

if __name__ == "__main__":
    # File path to your data
    file_path = "data/BTC_2019_2023_1h.csv"  # Using 1-hour timeframe data
    
    # Load and prepare data
    data = load_and_prepare_data(file_path)
    
    # Run backtest
    stats, bt = run_backtest(data)
    
    # Print metrics
    print_metrics(stats)
    
    # Plot the results
    bt.plot()
