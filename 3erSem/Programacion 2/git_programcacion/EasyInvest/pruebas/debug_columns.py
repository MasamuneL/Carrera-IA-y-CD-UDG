import yfinance as yf
import pandas as pd

# Test data download
symbol = "AAPL"
df = yf.download(symbol, period="5d", interval="1d")
print("Original columns:", df.columns)
print("Column type:", type(df.columns))
print("Data shape:", df.shape)
print("First few rows:")
print(df.head())

if isinstance(df.columns, pd.MultiIndex):
    print("MultiIndex levels:", df.columns.levels)
    print("Level 0:", df.columns.get_level_values(0))
    print("Level 1:", df.columns.get_level_values(1))
