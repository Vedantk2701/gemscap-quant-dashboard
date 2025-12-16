import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import time

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Gemscap Quant App", layout="wide")
st.title("📊 Gemscap Quantitative Analytics Dashboard")

# ---------------- Session State ----------------
if "prices" not in st.session_state:
    st.session_state.prices = []

MAX_POINTS = 200

# ---------------- Fetch Live Price ----------------
def fetch_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url, timeout=5).json()
    return float(data["price"])

# ---------------- Update Data ----------------
try:
    price = fetch_btc_price()
    st.session_state.prices.append({
        "time": datetime.now(),
        "price": price
    })

    if len(st.session_state.prices) > MAX_POINTS:
        st.session_state.prices.pop(0)

except Exception as e:
    st.error("Error fetching market data")

# ---------------- UI ----------------
if st.session_state.prices:
    df = pd.DataFrame(st.session_state.prices)

    # ---------- Quant Calculations ----------
    df["return"] = df["price"].pct_change()

    WINDOW = 30
    df["zscore"] = (
        df["price"] - df["price"].rolling(WINDOW).mean()
    ) / df["price"].rolling(WINDOW).std()

    # ---------- Latest Values ----------
    latest_price = df["price"].iloc[-1]
    latest_return = df["return"].iloc[-1]
    latest_z = df["zscore"].iloc[-1]

    # ---------- Trading Signal ----------
    if latest_z > 2:
        signal = "SELL 🔴"
    elif latest_z < -2:
        signal = "BUY 🟢"
    else:
        signal = "HOLD ⚪"

    # ---------- Metrics Layout ----------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="BTCUSDT Live Price",
        value=f"${latest_price:,.2f}"
    )

    col2.metric(
        label="BTCUSDT Return (last tick)",
        value=f"{latest_return * 100:.4f} %"
    )

    col3.metric(
        label="Trading Signal",
        value=signal
    )

    # ---------- Price Chart ----------
    fig_price = px.line(
        df,
        x="time",
        y="price",
        title="BTCUSDT Live Price Movement"
    )

    st.plotly_chart(fig_price, use_container_width=True)

    # ---------- Z-Score Chart ----------
    fig_z = px.line(
        df,
        x="time",
        y="zscore",
        title="BTCUSDT Z-Score (Mean Reversion Signal)"
    )

    st.plotly_chart(fig_z, use_container_width=True)

else:
    st.info("Waiting for live market data...")


# ---------------- Auto Refresh ----------------
time.sleep(1)
st.rerun()
