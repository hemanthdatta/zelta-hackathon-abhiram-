import os
import pandas as pd
import requests
from datetime import datetime
import time

def download_btc_data():
    # Create data directory if it doesn't exist
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Download data from Google Drive
    url = "https://drive.google.com/drive/folders/1VloVIKEbdcpTJgE_JqAJyBeARFnIlGsP"
    
    print(f"Please download the BTC/USDT data from: {url}")
    print("After downloading, place the CSV file in the 'data' directory")
    print("Then run the trading_strategy.py script")

if __name__ == "__main__":
    download_btc_data()
