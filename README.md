# 📊 Gemscap Quantitative Analytics Dashboard

This project is a real-time **Pairs Trading Quantitative Analytics Dashboard** developed as part of the **Gemscap Quantitative Developer Intern Assignment**.

The application demonstrates a **mean-reversion based pairs trading strategy** using live cryptocurrency market data sourced from the **Binance Public REST API**. It showcases real-time data ingestion, aggregation, quantitative analytics, alert generation, and interactive visualization.

---

## 🚀 Features

- Live price data ingestion for BTCUSDT and ETHUSDT
- User-selectable Y and X trading symbols
- Real-time **price spread** computation
- Rolling mean & rolling standard deviation
- **Z-score based mean reversion analysis**
- BUY / SELL / HOLD trading signals
- **Mean Reversion Half-Life** estimation
- Auto-refresh interval control
- Interactive Plotly charts (dark theme)
- Side-by-side visualization of:
  - Price Spread
  - Z-Score with threshold levels
- Real-time alert generation based on analytics
- CSV download of aggregated spread and z-score data
- Optional OHLC CSV upload support

---

## 📊 Real-Time Data Ingestion & Aggregation

The application continuously ingests real-time market prices from the Binance Public REST API and aggregates them in-memory using Pandas DataFrames.

- Each incoming price tick is timestamped during runtime
- Data is aggregated using Streamlit session state
- Rolling-window statistics are computed dynamically
- Analytics are enabled progressively as sufficient data becomes available
- No analytics requiring more than **intraday data** are used

This design ensures low-latency processing and real-time responsiveness.

---

## 📈 Quantitative Analytics Methodology

### Spread Calculation

### Rolling Statistics
- Rolling Mean computed over a user-defined window
- Rolling Standard Deviation computed over the same window

### Z-Score Calculation

### Trading Signal Logic
- **Z > +2** → SELL Y / BUY X  
- **Z < −2** → BUY Y / SELL X  
- Otherwise → HOLD  

This approach is widely used in quantitative trading systems to identify temporary mispricing between correlated assets.

---

## ⏱ Mean Reversion Half-Life

The mean reversion half-life estimates how quickly the spread reverts to its mean.

- Computed using linear regression on lagged spread changes
- Indicates the speed of convergence toward equilibrium
- Displayed dynamically once sufficient data is available

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** (Frontend & UI)
- **Pandas** (Data aggregation & analytics)
- **NumPy** (Statistical calculations)
- **Plotly** (Interactive visualizations)
- **Binance Public REST API** (Market data source)

---

## ▶ How to Run the Application

```bash
pip install -r requirements.txt
streamlit run app.py
