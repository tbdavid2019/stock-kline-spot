import yfinance as yf
import talib
import pandas as pd
import gradio as gr
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ------------------------------------------------------
# 1) 蠟燭形態對照表（中文） + 偵測函式
# ------------------------------------------------------
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

def detect_candlestick_patterns(data):
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
    for name, func in patterns.items():
        results[name] = func(open_prices, high_prices, low_prices, close_prices)
    return pd.DataFrame(results, index=data.index)


# ------------------------------------------------------
# 2) 常用形態分類
# ------------------------------------------------------
COMMON_PATTERNS = {
    "看漲形態": [
        "CDLMORNINGSTAR",
        "CDLMORNINGDOJISTAR",
        "CDLHAMMER",
        "CDLINVERTEDHAMMER",
        "CDLENGULFING",
        "CDLPIERCING",
        "CDL3WHITESOLDIERS",
        "CDLHARAMI",
        "CDLINNECK",
        "CDLONNECK",
        "CDLBELTHOLD",
        "CDLHOMINGPIGEON",
        "CDLMATCHINGLOW",
        "CDLTHRUSTING",
        "CDLUNIQUE3RIVER",
        "CDLLADDERBOTTOM",
        "CDLMARUBOZU"
    ],
    "看跌形態": [
        "CDLEVENINGSTAR",
        "CDLEVENINGDOJISTAR",
        "CDLHANGINGMAN",
        "CDLSHOOTINGSTAR",
        "CDLDARKCLOUDCOVER",
        "CDL3BLACKCROWS",
        "CDL2CROWS",
        "CDL3STARSINSOUTH",
        "CDLIDENTICAL3CROWS",
        "CDLADVANCEBLOCK",
        "CDLBREAKAWAY",
        "CDLCOUNTERATTACK",
        "CDLGAPSIDESIDEWHITE",
        "CDLGRAVESTONEDOJI",
        "CDLHIGHWAVE",
        "CDLSTALLEDPATTERN",
        "CDLUPSIDEGAP2CROWS",
        "CDLXSIDEGAP3METHODS"
    ]
}


# ------------------------------------------------------
# 3) 技術指標計算 (完整清單)
# ------------------------------------------------------
TECHNICAL_INDICATORS = [
    # Overlap Studies
    "MA", "SMA", "EMA", "WMA", "DEMA", "TEMA", "TRIMA", "KAMA", "BBANDS", "SAR", "MIDPOINT", "MIDPRICE",
    # Momentum Indicators
    "RSI", "STOCH", "STOCHF", "STOCHRSI", "MACD", "TRIX", "WILLR", "ADX", "ADXR", "APO", "AROON", "AROONOSC",
    "CCI", "CMO", "MFI", "MOM", "PPO", "ROC", "ULTOSC",
    # Volume Indicators
    "AD", "ADOSC", "OBV",
    # Volatility Indicators
    "TRANGE", "ATR", "NATR",
    # Price Transform
    "AVGPRICE", "MEDPRICE", "TYPPRICE", "WCLPRICE"
]

def calculate_selected_indicators(data, selected_indicators):
    """
    根據使用者勾選，動態計算各種技術指標並回傳 DataFrame
    """
    indicators = {}
    close_prices = data['Close'].values
    high_prices = data['High'].values
    low_prices = data['Low'].values
    volume = data['Volume'].values if 'Volume' in data.columns else None
    open_prices = data['Open'].values

    # Overlap Studies
    if "MA" in selected_indicators:
        indicators['MA'] = talib.MA(close_prices)
    if "SMA" in selected_indicators:
        indicators['SMA_30'] = talib.SMA(close_prices, timeperiod=30)
    if "EMA" in selected_indicators:
        indicators['EMA_30'] = talib.EMA(close_prices, timeperiod=30)
    if "WMA" in selected_indicators:
        indicators['WMA_30'] = talib.WMA(close_prices, timeperiod=30)
    if "DEMA" in selected_indicators:
        indicators['DEMA_30'] = talib.DEMA(close_prices, timeperiod=30)
    if "TEMA" in selected_indicators:
        indicators['TEMA_30'] = talib.TEMA(close_prices, timeperiod=30)
    if "TRIMA" in selected_indicators:
        indicators['TRIMA_30'] = talib.TRIMA(close_prices, timeperiod=30)
    if "KAMA" in selected_indicators:
        indicators['KAMA_30'] = talib.KAMA(close_prices, timeperiod=30)
    if "BBANDS" in selected_indicators:
        upper, middle, lower = talib.BBANDS(close_prices, timeperiod=20)
        indicators['BBANDS_Upper'] = upper
        indicators['BBANDS_Middle'] = middle
        indicators['BBANDS_Lower'] = lower
    if "SAR" in selected_indicators:
        indicators['SAR'] = talib.SAR(high_prices, low_prices, acceleration=0.02, maximum=0.2)
    if "MIDPOINT" in selected_indicators:
        indicators['MIDPOINT'] = talib.MIDPOINT(close_prices, timeperiod=14)
    if "MIDPRICE" in selected_indicators:
        indicators['MIDPRICE'] = talib.MIDPRICE(high_prices, low_prices, timeperiod=14)

    # Momentum Indicators
    if "RSI" in selected_indicators:
        indicators['RSI_14'] = talib.RSI(close_prices, timeperiod=14)
    if "STOCH" in selected_indicators:
        slowk, slowd = talib.STOCH(high_prices, low_prices, close_prices)
        indicators['STOCH_%K'] = slowk
        indicators['STOCH_%D'] = slowd
    if "STOCHF" in selected_indicators:
        fastk, fastd = talib.STOCHF(high_prices, low_prices, close_prices)
        indicators['STOCHF_%K'] = fastk
        indicators['STOCHF_%D'] = fastd
    if "STOCHRSI" in selected_indicators:
        fastk, fastd = talib.STOCHRSI(close_prices, timeperiod=14)
        indicators['STOCHRSI_%K'] = fastk
        indicators['STOCHRSI_%D'] = fastd
    if "MACD" in selected_indicators:
        macd, signal, hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
        indicators['MACD'] = macd
        indicators['MACD_Signal'] = signal
        indicators['MACD_Hist'] = hist
    if "TRIX" in selected_indicators:
        indicators['TRIX'] = talib.TRIX(close_prices, timeperiod=30)
    if "WILLR" in selected_indicators:
        indicators['WILLR'] = talib.WILLR(high_prices, low_prices, close_prices, timeperiod=14)
    if "ADX" in selected_indicators:
        indicators['ADX'] = talib.ADX(high_prices, low_prices, close_prices, timeperiod=14)
    if "ADXR" in selected_indicators:
        indicators['ADXR'] = talib.ADXR(high_prices, low_prices, close_prices, timeperiod=14)
    if "APO" in selected_indicators:
        indicators['APO'] = talib.APO(close_prices, fastperiod=12, slowperiod=26)
    if "AROON" in selected_indicators:
        aroon_down, aroon_up = talib.AROON(high_prices, low_prices, timeperiod=14)
        indicators['AROON_Up'] = aroon_up
        indicators['AROON_Down'] = aroon_down
    if "AROONOSC" in selected_indicators:
        indicators['AROONOSC'] = talib.AROONOSC(high_prices, low_prices, timeperiod=14)
    if "CCI" in selected_indicators:
        indicators['CCI'] = talib.CCI(high_prices, low_prices, close_prices, timeperiod=14)
    if "CMO" in selected_indicators:
        indicators['CMO'] = talib.CMO(close_prices, timeperiod=14)
    if "MFI" in selected_indicators and volume is not None:
        indicators['MFI'] = talib.MFI(high_prices, low_prices, close_prices, volume, timeperiod=14)
    if "MOM" in selected_indicators:
        indicators['MOM'] = talib.MOM(close_prices, timeperiod=10)
    if "PPO" in selected_indicators:
        indicators['PPO'] = talib.PPO(close_prices, fastperiod=12, slowperiod=26)
    if "ROC" in selected_indicators:
        indicators['ROC'] = talib.ROC(close_prices, timeperiod=10)
    if "ULTOSC" in selected_indicators:
        indicators['ULTOSC'] = talib.ULTOSC(high_prices, low_prices, close_prices)

    # Volume Indicators
    if "AD" in selected_indicators and volume is not None:
        indicators['AD'] = talib.AD(high_prices, low_prices, close_prices, volume)
    if "ADOSC" in selected_indicators and volume is not None:
        indicators['ADOSC'] = talib.ADOSC(high_prices, low_prices, close_prices, volume)
    if "OBV" in selected_indicators and volume is not None:
        indicators['OBV'] = talib.OBV(close_prices, volume)

    # Volatility Indicators
    if "TRANGE" in selected_indicators:
        indicators['TRANGE'] = talib.TRANGE(high_prices, low_prices, close_prices)
    if "ATR" in selected_indicators:
        indicators['ATR'] = talib.ATR(high_prices, low_prices, close_prices, timeperiod=14)
    if "NATR" in selected_indicators:
        indicators['NATR'] = talib.NATR(high_prices, low_prices, close_prices, timeperiod=14)

    # Price Transform
    if "AVGPRICE" in selected_indicators:
        indicators['AVGPRICE'] = talib.AVGPRICE(open_prices, high_prices, low_prices, close_prices)
    if "MEDPRICE" in selected_indicators:
        indicators['MEDPRICE'] = talib.MEDPRICE(high_prices, low_prices)
    if "TYPPRICE" in selected_indicators:
        indicators['TYPPRICE'] = talib.TYPPRICE(high_prices, low_prices, close_prices)
    if "WCLPRICE" in selected_indicators:
        indicators['WCLPRICE'] = talib.WCLPRICE(high_prices, low_prices, close_prices)

    return pd.DataFrame(indicators, index=data.index)


# ------------------------------------------------------
# 4) 資料抓取
# ------------------------------------------------------
def fetch_stock_data(ticker, period='6mo'):
    data = yf.download(ticker, period=period)
    if data.empty:
        raise ValueError(f"{ticker} 在所選時間內無資料。")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    required_columns = ['Open', 'High', 'Low', 'Close']
    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"資料缺少必要欄位：{missing}")
    data = data.dropna(subset=required_columns)
    return data


# ------------------------------------------------------
# 5) 建立多子圖 (3 rows):
#    row=1: Candlestick + 蠟燭形態標記
#    row=2: Volume
#    row=3: 技術指標
# ------------------------------------------------------
def create_subplots_chart(data, patterns_df, tech_df):
    """
    建立一個包含 3 個子圖的 figure:
    - row=1: K 線 + 形態標記
    - row=2: 成交量
    - row=3: 技術指標
    """
    date_strings = [d.strftime('%Y-%m-%d') for d in data.index]

    # 產生 3x1 子圖, row_heights 可自行調整
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.4, 0.2, 0.4],
                        vertical_spacing=0.03)

    # (A) row=1, col=1 放 K 線
    fig.add_trace(
        go.Candlestick(
            x=date_strings,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='K線'
        ),
        row=1, col=1
    )

    # (B) row=1, col=1: 標記蠟燭形態
    if not patterns_df.empty:
        pattern_dates = patterns_df.index
        if len(pattern_dates) > 0:
            found_labels = []
            for dt in pattern_dates:
                row_data = patterns_df.loc[dt]
                shapes = row_data[row_data != 0].index.tolist()
                friendly = [pattern_descriptions.get(x, x) for x in shapes]
                found_labels.append('\n'.join(friendly))
            date_markers = [d.strftime('%Y-%m-%d') for d in pattern_dates]
            fig.add_trace(
                go.Scatter(
                    x=date_markers,
                    y=data.loc[pattern_dates, 'High'],
                    mode='markers+text',
                    marker=dict(symbol='triangle-down', size=15, color='red'),
                    text=found_labels,
                    textposition="top center",
                    name='形態標記'
                ),
                row=1, col=1
            )

    # (C) row=2, col=1: 成交量 (獨立子圖)
    fig.add_trace(
        go.Bar(
            x=date_strings,
            y=data['Volume'],
            name='成交量',
            marker_color='rgba(128,128,128,0.5)'
        ),
        row=2, col=1
    )

    # (D) row=3, col=1: 技術指標
    if not tech_df.empty:
        for col in tech_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=date_strings,
                    y=tech_df[col],
                    mode='lines',
                    name=col
                ),
                row=3, col=1
            )

    fig.update_layout(
        height=900,
        title="Candlestick Pattern & Technical Indicator Analysis by David888.com",
        xaxis_title="日期"
    )

    return fig


# ------------------------------------------------------
# 6) 主分析函式: 整合形態偵測、技術指標計算、以及繪製多子圖
# ------------------------------------------------------
def analyze_stock(ticker, period='6mo', pattern_types=None, signal_strength=0, selected_indicators=None):
    try:
        # 抓取股價資料
        data = fetch_stock_data(ticker, period)

        # (1) 蠟燭形態偵測
        all_patterns = detect_candlestick_patterns(data)

        # 依照勾選的形態群組，組出 columns
        if pattern_types and len(pattern_types) > 0:
            selected_cols = []
            for group in pattern_types:
                selected_cols.extend(COMMON_PATTERNS.get(group, []))
        else:
            selected_cols = all_patterns.columns

        # 信號強度過濾
        patterns_filtered = all_patterns[selected_cols]
        if signal_strength > 0:
            patterns_filtered = patterns_filtered[
                (patterns_filtered >= signal_strength) | (patterns_filtered <= -signal_strength)
            ]
        patterns_filtered = patterns_filtered[(patterns_filtered != 0).any(axis=1)]

        # (2) 技術指標
        tech_df = pd.DataFrame()
        if selected_indicators:
            tech_df = calculate_selected_indicators(data, selected_indicators)

        # (3) 建立多子圖 (3 rows)
        chart = create_subplots_chart(data, patterns_filtered, tech_df)

        # (4) 合併所有資訊到 results_df 方便下載
        results_df = pd.concat([data, all_patterns, tech_df], axis=1)

        # (5) 輸出 CSV
        os.makedirs('tmp', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join('tmp', f"stock_analysis_{ticker}_{timestamp}.csv")
        results_df.to_csv(filename)

        if results_df.empty:
            return pd.DataFrame({"Message": [f"{ticker} 無資料或無形態。"]}), None, filename
        return results_df, chart, filename
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]}), None, None


# ------------------------------------------------------
# 7) Gradio 介面
# ------------------------------------------------------
with gr.Blocks() as interface:
    gr.Markdown("# Candlestick Pattern & Technical Indicator Analysis by David888.com")
    gr.Markdown("請輸入股票代碼、時間區間，選擇欲偵測的蠟燭形態、訊號強度以及技術指標。")

    with gr.Row():
        ticker_input = gr.Textbox(label="股票代碼", placeholder="例如：AAPL")
        period_input = gr.Dropdown(
            label="時間區間",
            choices=["1mo", "3mo", "6mo", "1y"],
            value="3mo"
        )
    with gr.Row():
        pattern_type = gr.CheckboxGroup(
            label="蠟燭形態類型",
            choices=["看漲形態", "看跌形態"],
            value=["看漲形態", "看跌形態"]
        )
        signal_strength = gr.Slider(
            label="訊號強度 (0=不過濾)",
            minimum=0,
            maximum=100,
            value=0,
            step=10
        )
    with gr.Row():
        indicator_selector = gr.CheckboxGroup(
            label="技術指標 (可多選)",
            choices=TECHNICAL_INDICATORS,
            value=["MACD", "RSI", "BBANDS"]  # 可自行調整預設勾選
        )
    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn = gr.Button("Clear")

    with gr.Column():
        chart_output = gr.Plot(label="分析圖")
        output_table = gr.Dataframe(label="分析結果")
        file_output = gr.File(label="下載 CSV")

    def process_input(ticker, period, selected_patterns, strength, selected_indicators):
        return analyze_stock(ticker, period, selected_patterns, strength, selected_indicators)

    submit_btn.click(
        fn=process_input,
        inputs=[ticker_input, period_input, pattern_type, signal_strength, indicator_selector],
        outputs=[output_table, chart_output, file_output]
    )

    clear_btn.click(
        fn=lambda: (None, None, None),
        inputs=[],
        outputs=[output_table, chart_output, file_output]
    )

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=5678, share=False)