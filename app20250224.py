import yfinance as yf
import talib
import pandas as pd
import gradio as gr
from datetime import datetime
import plotly.graph_objects as go
import numpy as np
import os

# (1) 定義「形態名稱對照表」：可將 CDLxxxx 對應到更易懂的名稱
pattern_descriptions = {
    "CDL2CROWS": "雙鴉（CDL2CROWS）",
    "CDL3BLACKCROWS": "三烏鴉（CDL3BLACKCROWS）",
    "CDL3INSIDE": "內困三日上升 / 下降（CDL3INSIDE）",
    "CDL3LINESTRIKE": "三線打擊（CDL3LINESTRIKE）",
    "CDL3OUTSIDE": "外側三日上升 / 下降（CDL3OUTSIDE）",
    "CDL3STARSINSOUTH": "南方三星（CDL3STARSINSOUTH）",
    "CDL3WHITESOLDIERS": "三白兵（CDL3WHITESOLDIERS）",
    "CDLABANDONEDBABY": "棄嬰（CDLABANDONEDBABY）",
    "CDLADVANCEBLOCK": "大敵當前（CDLADVANCEBLOCK）",
    "CDLBELTHOLD": "捉腰帶線（CDLBELTHOLD）",
    "CDLBREAKAWAY": "脫離（CDLBREAKAWAY）",
    "CDLCLOSINGMARUBOZU": "收盤缺影線（CDLCLOSINGMARUBOZU）",
    "CDLCONCEALBABYSWALL": "藏嬰吞沒（CDLCONCEALBABYSWALL）",
    "CDLCOUNTERATTACK": "反擊線（CDLCOUNTERATTACK）",
    "CDLDARKCLOUDCOVER": "烏雲壓頂（CDLDARKCLOUDCOVER）",
    "CDLDOJI": "十字（CDLDOJI）",
    "CDLDOJISTAR": "十字星（CDLDOJISTAR）",
    "CDLDRAGONFLYDOJI": "蜻蜓十字（CDLDRAGONFLYDOJI）",
    "CDLENGULFING": "吞噬模式（CDLENGULFING）",
    "CDLEVENINGDOJISTAR": "十字暮星（CDLEVENINGDOJISTAR）",
    "CDLEVENINGSTAR": "暮星（CDLEVENINGSTAR）",
    "CDLGAPSIDESIDEWHITE": "向上 / 下跳空並列陽線（CDLGAPSIDESIDEWHITE）",
    "CDLGRAVESTONEDOJI": "墓碑十字（CDLGRAVESTONEDOJI）",
    "CDLHAMMER": "錘頭（CDLHAMMER）",
    "CDLHANGINGMAN": "上吊線（CDLHANGINGMAN）",
    "CDLHARAMI": "母子線（CDLHARAMI）",
    "CDLHARAMICROSS": "十字孕線（CDLHARAMICROSS）",
    "CDLHIGHWAVE": "風高浪大線（CDLHIGHWAVE）",
    "CDLHIKKAKE": "陷阱（CDLHIKKAKE）",
    "CDLHIKKAKEMOD": "修正陷阱（CDLHIKKAKEMOD）",
    "CDLHOMINGPIGEON": "家鴿（CDLHOMINGPIGEON）",
    "CDLIDENTICAL3CROWS": "三胞胎烏鴉（CDLIDENTICAL3CROWS）",
    "CDLINNECK": "頸內線（CDLINNECK）",
    "CDLINVERTEDHAMMER": "倒錘頭（CDLINVERTEDHAMMER）",
    "CDLKICKING": "反衝型態（CDLKICKING）",
    "CDLKICKINGBYLENGTH": "由較長缺影線決定的反衝型態（CDLKICKINGBYLENGTH）",
    "CDLLADDERBOTTOM": "梯底（CDLLADDERBOTTOM）",
    "CDLLONGLEGGEDDOJI": "長腳十字（CDLLONGLEGGEDDOJI）",
    "CDLLONGLINE": "長蠟燭（CDLLONGLINE）",
    "CDLMARUBOZU": "光頭光腳 / 缺影線（CDLMARUBOZU）",
    "CDLMATCHINGLOW": "相同低價（CDLMATCHINGLOW）",
    "CDLMATHOLD": "鋪墊（CDLMATHOLD）",
    "CDLMORNINGDOJISTAR": "十字晨星（CDLMORNINGDOJISTAR）",
    "CDLMORNINGSTAR": "晨星（CDLMORNINGSTAR）",
    "CDLONNECK": "頸上線（CDLONNECK）",
    "CDLPIERCING": "刺透（CDLPIERCING）",
    "CDLRICKSHAWMAN": "黃包車伕（CDLRICKSHAWMAN）",
    "CDLRISEFALL3METHODS": "上升 / 下降三法（CDLRISEFALL3METHODS）",
    "CDLSEPARATINGLINES": "分離線（CDLSEPARATINGLINES）",
    "CDLSHOOTINGSTAR": "射擊之星（CDLSHOOTINGSTAR）",
    "CDLSHORTLINE": "短蠟燭（CDLSHORTLINE）",
    "CDLSPINNINGTOP": "紡錘（CDLSPINNINGTOP）",
    "CDLSTALLEDPATTERN": "停頓（CDLSTALLEDPATTERN）",
    "CDLSTICKSANDWICH": "條形三明治（CDLSTICKSANDWICH）",
    "CDLTAKURI": "探水竿（CDLTAKURI）",
    "CDLTASUKIGAP": "跳空並列陰陽線（CDLTASUKIGAP）",
    "CDLTHRUSTING": "插入（CDLTHRUSTING）",
    "CDLTRISTAR": "三星（CDLTRISTAR）",
    "CDLUNIQUE3RIVER": "奇特三河床（CDLUNIQUE3RIVER）",
    "CDLUPSIDEGAP2CROWS": "向上跳空雙烏鴉（CDLUPSIDEGAP2CROWS）",
    "CDLXSIDEGAP3METHODS": "上升 / 下降跳空三法（CDLXSIDEGAP3METHODS）"
}


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
    fig.add_trace(go.Bar(
        x=date_strings, 
        y=data['Volume'],
        name='成交量',
        yaxis='y2',
        marker_color='rgba(128,128,128,0.5)'
    ))
    
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
        
        # 更新結果 DataFrame，只留下有出現形態的列
        results_df = pd.concat([data, filtered_patterns], axis=1)
        results_df = results_df[(filtered_patterns != 0).any(axis=1)]
        
        # 創建圖表
        chart = create_candlestick_chart(data)
        
        # (2) 標記過濾後的形態位置時，轉成「中文 / 更友善」名稱
        pattern_dates = results_df.index
        pattern_names = []
        
        for date in pattern_dates:
            patterns_on_date = filtered_patterns.loc[date]
            # 取出當日 != 0 的形態 (代表出現訊號)
            found_patterns = patterns_on_date[patterns_on_date != 0].index.tolist()
            # 將每個 CDLxxxx 轉成中文描述 (若字典裡沒有就顯示原始 key)
            friendly_names = [pattern_descriptions.get(p, p) for p in found_patterns]
            pattern_names.append('\n'.join(friendly_names))
        
        if len(pattern_dates) > 0:
            date_strings = [d.strftime('%Y-%m-%d') for d in pattern_dates]
            # 在圖表上加一個散點圖層，顯示形態文字
            chart.add_trace(go.Scatter(
                x=date_strings,
                y=data.loc[pattern_dates, 'High'],
                mode='markers+text',
                marker=dict(symbol='triangle-down', size=15, color='red'),
                text=pattern_names,        # 顯示更友善的文字
                textposition="top center",
                name='形態標記'
            ))
        
        # 確保 tmp 文件夾存在
        os.makedirs('tmp', exist_ok=True)

        # 儲存 CSV 到 tmp/ 文件夾
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join('tmp', f"stock_analysis_{ticker}_{timestamp}.csv")
        results_df.to_csv(filename)
        
        if results_df.empty:
            return pd.DataFrame({"Message": [f"No patterns detected for {ticker}."]}), None, filename
        return results_df, chart, filename
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), None, None


# 定義常用的蠟燭圖形態
COMMON_PATTERNS = {
    "看漲形態": [
        "CDLMORNINGSTAR",     # 晨星
        "CDLMORNINGDOJISTAR", # 晨星十字星
        "CDLHAMMER",          # 錘子線
        "CDLINVERTEDHAMMER",  # 倒錘子線
        "CDLENGULFING",       # 吞沒形態(看漲)
        "CDLPIERCING",        # 穿刺線
        "CDL3WHITESOLDIERS",  # 三白兵
        "CDLHARAMI",          # 懷孕線(看漲)
        "CDLINNECK",          # 內頸線
        "CDLONNECK",          # 上頸線
        "CDLBELTHOLD",        # 捉腰帶線(看漲)
        "CDLHOMINGPIGEON",    # 返家鴿
        "CDLMATCHINGLOW",     # 相同低點
        "CDLTHRUSTING",       # 戳入線
        "CDLUNIQUE3RIVER",    # 獨特三河
        "CDLLADDERBOTTOM",    # 梯底
        "CDLMARUBOZU",        # 光頭光腳/缺影線(看漲)
        "CDLTAKURI"           # 探水竿
    ],
    "看跌形態": [
        "CDLEVENINGSTAR",     # 暮星
        "CDLEVENINGDOJISTAR", # 暮星十字星
        "CDLHANGINGMAN",      # 上吊線
        "CDLSHOOTINGSTAR",    # 流星
        "CDLDARKCLOUDCOVER",  # 烏雲蓋頂
        "CDL3BLACKCROWS",     # 三隻烏鴉
        "CDL2CROWS",          # 二烏鴉
        "CDL3STARSINSOUTH",   # 南方三星
        "CDLIDENTICAL3CROWS", # 三隻相同烏鴉
        "CDLADVANCEBLOCK",    # 大敗形態
        "CDLBREAKAWAY",       # 脫離形態(看跌)
        "CDLCOUNTERATTACK",   # 反擊線(看跌)
        "CDLGAPSIDESIDEWHITE",# 向下跳空並列陰線
        "CDLGRAVESTONEDOJI",  # 墓碑十字線
        "CDLHIGHWAVE",        # 長腳十字(看跌)
        "CDLSTALLEDPATTERN",  # 停頓形態
        "CDLUPSIDEGAP2CROWS", # 上升跳空兩烏鴉
        "CDLXSIDEGAP3METHODS" # 跳空三法(看跌)
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
        for pattern_type_key in selected_patterns:
            pattern_list.extend(COMMON_PATTERNS[pattern_type_key])
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
    interface.launch(
        server_name="0.0.0.0",  # 允許外部訪問
        server_port=5678,      # 指定端口
        share=False            # 不使用 Gradio 的分享功能
    )