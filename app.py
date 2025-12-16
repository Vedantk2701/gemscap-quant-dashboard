import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import time
import numpy as np

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Gemscap Quant App", layout="wide")
st.title("📊 Gemscap Quantitative Analytics Dashboard")

# ---------------- Session State ----------------
if "prices" not in st.session_state:
    st.session_state.prices = []

MAX_POINTS = 200

# ---------------- Controls ----------------
st.subheader("Pairs Trading Analytics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    y_symbol = st.selectbox("Y Symbol", ["BTCUSDT", "ETHUSDT"], index=0)

with c2:
    x_symbol = st.selectbox("X Symbol", ["ETHUSDT", "BTCUSDT"], index=0)

with c3:
    WINDOW = st.slider("Rolling Window", 10, 60, 30)

with c4:
    refresh_interval = st.slider("Auto-refresh interval (seconds)", 1, 30, 1)

# ---------------- Fetch Price ----------------
def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url, timeout=5).json()["price"])

# ---------------- Update Data ----------------
try:
    y_price = fetch_price(y_symbol)
    x_price = fetch_price(x_symbol)

    st.session_state.prices.append({
        "time": datetime.now(),
        "y": y_price,
        "x": x_price
    })

    if len(st.session_state.prices) > MAX_POINTS:
        st.session_state.prices.pop(0)

except Exception:
    st.error("Error fetching market data")

# ---------------- UI ----------------
if st.session_state.prices:
    df = pd.DataFrame(st.session_state.prices)

    # ---------- Quant Calculations ----------
    df["spread"] = df["y"] - df["x"]
    df["spread_mean"] = df["spread"].rolling(WINDOW).mean()
    df["spread_std"] = df["spread"].rolling(WINDOW).std()
    df["zscore"] = (df["spread"] - df["spread_mean"]) / df["spread_std"]

    latest_y = df["y"].iloc[-1]
    latest_x = df["x"].iloc[-1]
    latest_z = df["zscore"].iloc[-1]

    # ---------- Mean Reversion Half-Life ----------
    spread_lag = df["spread"].shift(1)
    spread_ret = df["spread"] - spread_lag
    spread_lag = spread_lag.dropna()
    spread_ret = spread_ret.dropna()

    if len(spread_lag) > 5:
        beta = np.polyfit(spread_lag, spread_ret, 1)[0]
        half_life = -np.log(2) / beta if beta < 0 else np.nan
    else:
        half_life = np.nan

    # ---------- Trading Signal ----------
    if latest_z > 2:
        signal = "SELL Y / BUY X 🔴"
        alert = "Spread is HIGH → Mean reversion SELL signal"
    elif latest_z < -2:
        signal = "BUY Y / SELL X 🟢"
        alert = "Spread is LOW → Mean reversion BUY signal"
    else:
        signal = "HOLD ⚪"
        alert = "No active alerts"

    # ---------- Metrics ----------
    m1, m2, m3 = st.columns(3)
    m1.metric(f"{y_symbol} Price", f"${latest_y:,.2f}")
    m2.metric(f"{x_symbol} Price", f"${latest_x:,.2f}")
    m3.metric("Trading Signal", signal)

    # ---------- Charts Side by Side ----------
    ch1, ch2 = st.columns(2)

    with ch1:
        fig_spread = px.line(
            df,
            x="time",
            y="spread",
            title="Price Spread",
            template="plotly_dark"
        )
        st.plotly_chart(fig_spread, use_container_width=True)

    with ch2:
        fig_z = px.line(
            df,
            x="time",
            y="zscore",
            title="Z-Score (Mean Reversion)",
            template="plotly_dark"
        )
        fig_z.add_hline(y=2, line_dash="dash", line_color="red")
        fig_z.add_hline(y=-2, line_dash="dash", line_color="green")
        st.plotly_chart(fig_z, use_container_width=True)

    # ---------- CSV Download ----------
    csv = df[["time", "spread", "zscore"]].to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Spread Data (CSV)",
        csv,
        "spread_data.csv",
        "text/csv"
    )

    # ---------- Half-Life ----------
    st.markdown("### Mean Reversion Half-Life (sec)")
    st.metric("", f"{half_life:.2f}" if not np.isnan(half_life) else "Calculating...")

    # ---------- Alerts ----------
    st.markdown("### Alerts")
    if "BUY" in alert:
        st.success(alert)
    elif "SELL" in alert:
        st.error(alert)
    else:
        st.info(alert)

else:
    st.info("Waiting for live market data...")

# ---------------- Auto Refresh ----------------
time.sleep(refresh_interval)
st.rerun()
