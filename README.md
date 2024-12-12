蠟燭圖形態辨識工具 DAVID888

此工具透過 yfinance 提取股票數據，並使用 TA-Lib 識別股票的蠟燭圖形態，並生成詳細的結果，包括圖表和檢測到的形態列表。

功能
	1.	支援多種股票市場數據，包括美股和台股。
	2.	自動辨識常見蠟燭圖形態（如晨星、三白兵等）。
	3.	可視化的 K 線圖和成交量柱狀圖，並標註檢測到的形態。
	4.	支援選擇特定的形態類型（看漲形態、看跌形態）。
	5.	將分析結果匯出為 CSV 檔案供下載。

安裝指引

1. 安裝必要的 Python 套件

pip install yfinance ta-lib pandas gradio plotly numpy

	注意：在安裝 TA-Lib 前，請確保已安裝 TA-Lib 的系統庫。具體指引請參考 TA-Lib 官方網站。

使用方法

執行程式

python app.py

功能介面
	1.	輸入股票代碼（例如 AAPL 或 2330.TW）。
	2.	選擇分析的時間範圍（1 個月至 1 年）。
	3.	選擇分析的蠟燭圖形態類型（看漲或看跌形態）。
	4.	調整信號強度篩選（預設為 0 表示顯示所有檢測到的形態）。
	5.	點擊 Submit 按鈕檢視分析結果。

功能說明
	•	K 線圖與成交量圖： 顯示股票的價格走勢與成交量，並標註檢測到的形態位置。
	•	形態檢測表格： 詳細列出檢測到的蠟燭圖形態，並顯示每個形態的信號強度。
	•	下載結果： 將檢測結果匯出為 CSV 檔案供後續分析。

範例

1. 輸入股票代碼與設定
	•	股票代碼：2330.TW
	•	時間範圍：6 個月
	•	選擇形態類型：看漲形態
	•	信號強度：20

2. 輸出結果
	1.	K 線圖：包含成交量和檢測到的形態標記。
	2.	表格：檢測到的形態及其出現的時間與信號強度。
	3.	匯出：下載分析結果的 CSV 檔案。

Candlestick Pattern Recognition Tool

This tool leverages yfinance to fetch stock data and uses TA-Lib to detect candlestick patterns. It provides detailed results, including visual charts and a list of detected patterns.

Features
	1.	Supports multiple stock markets, including US and Taiwan stocks.
	2.	Automatically detects common candlestick patterns (e.g., Morning Star, Three White Soldiers).
	3.	Visualizes candlestick charts with volume bars and highlights detected patterns.
	4.	Allows selecting specific pattern types (Bullish or Bearish patterns).
	5.	Exports analysis results as a downloadable CSV file.

Installation Guide

1. Install Required Python Libraries

pip install yfinance ta-lib pandas gradio plotly numpy

	Note: Before installing the TA-Lib Python package, ensure the TA-Lib system library is installed. Refer to the TA-Lib Official Documentation for setup instructions.

Usage Instructions

Run the Application

python app.py

Interface Features
	1.	Enter the stock ticker (e.g., AAPL or 2330.TW).
	2.	Select the time period for analysis (1 month to 1 year).
	3.	Choose the types of candlestick patterns to detect (Bullish or Bearish).
	4.	Adjust the signal strength filter (default is 0 to show all detected patterns).
	5.	Click the Submit button to view the analysis results.

Feature Highlights
	•	Candlestick and Volume Charts: Displays the stock price trends and volume, with detected patterns marked on the chart.
	•	Pattern Detection Table: Lists detected candlestick patterns with their occurrence time and signal strength.
	•	Downloadable Results: Exports the analysis results as a CSV file for further analysis.

Example

1. Input Stock Ticker and Settings
	•	Stock Ticker: 2330.TW
	•	Time Period: 6 months
	•	Selected Pattern Type: Bullish Patterns
	•	Signal Strength: 20

2. Output Results
	1.	Candlestick Chart: Includes volume bars and detected pattern markers.
	2.	Table: Details detected patterns, their occurrence, and signal strength.
	3.	Export: Download the analysis results as a CSV file.

Enjoy analyzing stock candlestick patterns!