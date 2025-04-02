import yfinance as yf
import pandas as pd
import schedule
import time
from datetime import datetime
import os
from etf_strategy_config import etf_strategies
from notifier import send_kakao_message


# 로그 디렉토리 생성
os.makedirs("logs", exist_ok=True)

# RSI 계산
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# 이동평균 계산
def compute_sma(series, period=20):
    return series.rolling(window=period).mean()

# 분석 실행
def check_etf(ticker, config):
    try:
        df = yf.download(ticker, period="60d", interval="1d", progress=False)
        if df.empty:
            print(f"[{ticker}] 데이터 없음")
            return

        df["RSI"] = compute_rsi(df["Close"])
        df["SMA20"] = compute_sma(df["Close"])
        latest_rsi = df["RSI"].iloc[-1]
        latest_price = df["Close"].iloc[-1].item()
        sma20 = df["SMA20"].iloc[-1]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        signal = None

        print(f"{ticker} → RSI: {latest_rsi}, 종가: {latest_price}, SMA20: {sma20}")

##        if pd.isna(latest_rsi) or pd.isna(latest_price) or pd.isna(sma20):
##            print(f"[{ticker}] 최근 값 중 NaN 존재 (분석 스킵)")
##            return

        # 매수 조건
        if latest_rsi < config["buy_rsi"] and latest_price > sma20:
            signal = f"[{now}] {config['name']} → 매수 타이밍! (RSI={latest_rsi:.2f}, 종가>{sma20:.2f})"
            send_kakao_message(signal)  # ✅ 카카오톡으로 알림

        # 과열 경고 조건
        elif latest_rsi > config["overheat_rsi"] and latest_price < sma20:
            signal = f"[{now}] {config['name']} → 과열 주의 (RSI={latest_rsi:.2f}, 종가<{sma20:.2f})"
            send_kakao_message(signal)  # ✅ 카카오톡으로 알림

        else:
            signal = f"[{now}] {config['name']} → 정상 (RSI={latest_rsi:.2f}, SMA20={sma20:.2f})"

        print(signal)
        with open("logs/rsi_alerts.log", "a") as f:
            f.write(signal + "\n")

    except Exception as e:
        print(f"[오류] {ticker}: {e}")

# 전체 ETF 분석 실행
def job():
    for ticker, config in etf_strategies.items():
        check_etf(ticker, config)

# 스케줄 실행
schedule.every(5).minutes.do(job)

print("=== RSI + 이동평균선 조건 ETF 분석 시작 ===")
job()
while True:
    schedule.run_pending()
    time.sleep(1)
