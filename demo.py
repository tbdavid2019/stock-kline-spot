import yfinance as yf

# 定義股票代碼，例如台積電
ticker = '2330.TW'

# 測試下載數據
data = yf.download(ticker, start='2024-01-01', end='2024-10-31')
print(data.head())