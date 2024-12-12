import yfinance as yf
import talib
import pandas as pd
import gradio as gr
from datetime import datetime
import plotly.graph_objects as go
import numpy as np

def create_candlestick_chart(data):
    # 將索引轉換為字符串格式
    date_strings = [d.strftime('%Y-%m-%d') for d in data.index]
    
    fig = go.Figure(data=[go.Candlestick(x=date_strings,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='K線')])
    
    # 添加成交量柱狀圖
    fig.add_trace(go.Bar(x=date_strings, 
                        y=data['Volume'],
                        name='成交量',
                        yaxis='y2',
                        marker_color='rgba(128,128,128,0.5)'))
    
    # 更新布局
    fig.update_layout(
        title='股票價格走勢圖',
        yaxis_title='價格',
        yaxis2=dict(
            title='成交量',
            overlaying='y',
            side='right'
        ),
        xaxis_title='日期',
        height=600
    )
    
    return fig


def fetch_stock_data(ticker, period='6mo'):
    try:
        data = yf.download(ticker, period=period)
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker} in the selected period.")
            
        # 處理 MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            # 將 MultiIndex columns 轉換為單層級
            data.columns = data.columns.get_level_values(0)
            
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Data missing required columns: {missing_columns}")
            
        data = data.dropna(subset=required_columns)
        for col in required_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
            
        if data[required_columns].isnull().any().any():
            raise ValueError(f"Data contains NaN values after processing for ticker {ticker}.")
            
        return data
    except Exception as e:
        raise ValueError(f"Failed to fetch data for ticker {ticker}. Reason: {str(e)}")

def detect_candlestick_patterns(data):
    required_columns = ['Open', 'High', 'Low', 'Close']
    if not all(col in data.columns for col in required_columns):
        raise ValueError("Required columns (Open, High, Low, Close) are missing in the data.")
    if data[required_columns].isnull().any().any():
        raise ValueError("Input data contains NaN values in required columns (Open, High, Low, Close).")

    if len(data) < 1:
        raise ValueError("Not enough data to perform candlestick pattern detection.")

    open_prices = data['Open'].values
    high_prices = data['High'].values
    low_prices = data['Low'].values
    close_prices = data['Close'].values

    patterns = {
        "CDL2CROWS": talib.CDL2CROWS,
        "CDL3BLACKCROWS": talib.CDL3BLACKCROWS,
        "CDL3INSIDE": talib.CDL3INSIDE,
        "CDL3LINESTRIKE": talib.CDL3LINESTRIKE,
        "CDL3OUTSIDE": talib.CDL3OUTSIDE,
        "CDL3STARSINSOUTH": talib.CDL3STARSINSOUTH,
        "CDL3WHITESOLDIERS": talib.CDL3WHITESOLDIERS,
        "CDLABANDONEDBABY": talib.CDLABANDONEDBABY,
        "CDLADVANCEBLOCK": talib.CDLADVANCEBLOCK,
        "CDLBELTHOLD": talib.CDLBELTHOLD,
        "CDLBREAKAWAY": talib.CDLBREAKAWAY,
        "CDLCLOSINGMARUBOZU": talib.CDLCLOSINGMARUBOZU,
        "CDLCONCEALBABYSWALL": talib.CDLCONCEALBABYSWALL,
        "CDLCOUNTERATTACK": talib.CDLCOUNTERATTACK,
        "CDLDARKCLOUDCOVER": talib.CDLDARKCLOUDCOVER,
        "CDLDOJI": talib.CDLDOJI,
        "CDLDOJISTAR": talib.CDLDOJISTAR,
        "CDLDRAGONFLYDOJI": talib.CDLDRAGONFLYDOJI,
        "CDLENGULFING": talib.CDLENGULFING,
        "CDLEVENINGDOJISTAR": talib.CDLEVENINGDOJISTAR,
        "CDLEVENINGSTAR": talib.CDLEVENINGSTAR,
        "CDLGAPSIDESIDEWHITE": talib.CDLGAPSIDESIDEWHITE,
        "CDLGRAVESTONEDOJI": talib.CDLGRAVESTONEDOJI,
        "CDLHAMMER": talib.CDLHAMMER,
        "CDLHANGINGMAN": talib.CDLHANGINGMAN,
        "CDLHARAMI": talib.CDLHARAMI,
        "CDLHARAMICROSS": talib.CDLHARAMICROSS,
        "CDLHIGHWAVE": talib.CDLHIGHWAVE,
        "CDLHIKKAKE": talib.CDLHIKKAKE,
        "CDLHIKKAKEMOD": talib.CDLHIKKAKEMOD,
        "CDLHOMINGPIGEON": talib.CDLHOMINGPIGEON,
        "CDLIDENTICAL3CROWS": talib.CDLIDENTICAL3CROWS,
        "CDLINNECK": talib.CDLINNECK,
        "CDLINVERTEDHAMMER": talib.CDLINVERTEDHAMMER,
        "CDLKICKING": talib.CDLKICKING,
        "CDLKICKINGBYLENGTH": talib.CDLKICKINGBYLENGTH,
        "CDLLADDERBOTTOM": talib.CDLLADDERBOTTOM,
        "CDLLONGLEGGEDDOJI": talib.CDLLONGLEGGEDDOJI,
        "CDLLONGLINE": talib.CDLLONGLINE,
        "CDLMARUBOZU": talib.CDLMARUBOZU,
        "CDLMATCHINGLOW": talib.CDLMATCHINGLOW,
        "CDLMATHOLD": talib.CDLMATHOLD,
        "CDLMORNINGDOJISTAR": talib.CDLMORNINGDOJISTAR,
        "CDLMORNINGSTAR": talib.CDLMORNINGSTAR,
        "CDLONNECK": talib.CDLONNECK,
        "CDLPIERCING": talib.CDLPIERCING,
        "CDLRICKSHAWMAN": talib.CDLRICKSHAWMAN,
        "CDLRISEFALL3METHODS": talib.CDLRISEFALL3METHODS,
        "CDLSEPARATINGLINES": talib.CDLSEPARATINGLINES,
        "CDLSHOOTINGSTAR": talib.CDLSHOOTINGSTAR,
        "CDLSHORTLINE": talib.CDLSHORTLINE,
        "CDLSPINNINGTOP": talib.CDLSPINNINGTOP,
        "CDLSTALLEDPATTERN": talib.CDLSTALLEDPATTERN,
        "CDLSTICKSANDWICH": talib.CDLSTICKSANDWICH,
        "CDLTAKURI": talib.CDLTAKURI,
        "CDLTASUKIGAP": talib.CDLTASUKIGAP,
        "CDLTHRUSTING": talib.CDLTHRUSTING,
        "CDLTRISTAR": talib.CDLTRISTAR,
        "CDLUNIQUE3RIVER": talib.CDLUNIQUE3RIVER,
        "CDLUPSIDEGAP2CROWS": talib.CDLUPSIDEGAP2CROWS,
        "CDLXSIDEGAP3METHODS": talib.CDLXSIDEGAP3METHODS,
    }

    results = {}
    for pattern_name, pattern_func in patterns.items():
        results[pattern_name] = pattern_func(open_prices, high_prices, low_prices, close_prices)
    return pd.DataFrame(results, index=data.index)

def analyze_stock(ticker, period='6mo', pattern_types=None, signal_strength=0):
    try:
        data = fetch_stock_data(ticker, period)
        patterns = detect_candlestick_patterns(data)
        results_df = pd.concat([data, patterns], axis=1)
        
        # 根據選擇的模式過濾
        if pattern_types and len(pattern_types) > 0:
            pattern_columns = pattern_types
        else:
            pattern_columns = patterns.columns

        # 只保留選擇的模式和符合信號強度的結果
        filtered_patterns = patterns[pattern_columns]
        if signal_strength > 0:
            filtered_patterns = filtered_patterns[
                (filtered_patterns >= signal_strength) | 
                (filtered_patterns <= -signal_strength)
            ]
        
        # 更新結果DataFrame
        results_df = pd.concat([data, filtered_patterns], axis=1)
        results_df = results_df[
            (filtered_patterns != 0).any(axis=1)
        ]
        
        # 創建圖表
        chart = create_candlestick_chart(data)
        
        # 標記過濾後的形態位置
        pattern_dates = results_df.index
        pattern_names = []
        for date in pattern_dates:
            patterns_on_date = filtered_patterns.loc[date]
            found_patterns = patterns_on_date[patterns_on_date != 0].index.tolist()
            pattern_names.append('\n'.join(found_patterns))
        
        if len(pattern_dates) > 0:
            date_strings = [d.strftime('%Y-%m-%d') for d in pattern_dates]
            chart.add_trace(go.Scatter(
                x=date_strings,
                y=data.loc[pattern_dates, 'High'],
                mode='markers+text',
                marker=dict(symbol='triangle-down', size=15, color='red'),
                text=pattern_names,
                textposition="top center",
                name='形態標記'
            ))
        
        # 儲存CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stock_analysis_{ticker}_{timestamp}.csv"
        results_df.to_csv(filename)
        
        if results_df.empty:
            return pd.DataFrame({"Message": [f"No patterns detected for {ticker}."]}), None, filename
        return results_df, chart, filename
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), None, None

# 定義常用的蠟燭圖形態
COMMON_PATTERNS = {
    "看漲形態": [
        "CDLMORNINGSTAR",    # 晨星
        "CDLMORNINGDOJISTAR", # 晨星十字星
        "CDLHAMMER",         # 錘子線
        "CDLINVERTEDHAMMER", # 倒錘子線
        "CDLENGULFING",      # 吞沒形態
        "CDLPIERCING",       # 穿刺線
        "CDL3WHITESOLDIERS"  # 三白兵
    ],
    "看跌形態": [
        "CDLEVENINGSTAR",    # 暮星
        "CDLEVENINGDOJISTAR", # 暮星十字星
        "CDLHANGINGMAN",     # 上吊線
        "CDLSHOOTINGSTAR",   # 流星
        "CDLDARKCLOUDCOVER", # 烏雲蓋頂
        "CDL3BLACKCROWS"     # 三黑鴉
    ]
}

with gr.Blocks() as interface:
    gr.Markdown("# Candlestick Pattern Recognition")
    gr.Markdown("Enter a stock ticker and select a time period to detect candlestick patterns.")
    
    with gr.Row():
        ticker_input = gr.Textbox(label="Stock Ticker", placeholder="e.g., AAPL")
        period_input = gr.Dropdown(
            label="Time Period", 
            choices=["1mo", "3mo", "6mo", "1y"], 
            value="6mo"
        )
    
    with gr.Row():
        pattern_type = gr.CheckboxGroup(
            label="Pattern Types",
            choices=[
                "看漲形態",
                "看跌形態"
            ],
            value=["看漲形態", "看跌形態"]
        )
        signal_strength = gr.Slider(
            label="Signal Strength",
            minimum=0,
            maximum=100,
            value=0,
            step=10
        )
    
    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn = gr.Button("Clear")
    
    with gr.Column():
        chart_output = gr.Plot(label="Stock Chart")
        output_table = gr.Dataframe(label="Candlestick Patterns Detected")
        file_output = gr.File(label="Download Results")

    def process_input(ticker, period, selected_patterns, strength):
        # 將選擇的模式類型轉換為具體的模式列表
        pattern_list = []
        for pattern_type in selected_patterns:
            pattern_list.extend(COMMON_PATTERNS[pattern_type])
        return analyze_stock(ticker, period, pattern_list, strength)

    submit_btn.click(
        fn=process_input,
        inputs=[ticker_input, period_input, pattern_type, signal_strength],
        outputs=[output_table, chart_output, file_output]
    )
    
    clear_btn.click(
        fn=lambda: (None, None, None),
        inputs=[],
        outputs=[output_table, chart_output, file_output]
    )

if __name__ == "__main__":
    interface.launch()