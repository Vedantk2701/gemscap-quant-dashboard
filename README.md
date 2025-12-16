# 📊 Gemscap Quantitative Analytics Dashboard

This project is a real-time **Pairs Trading Quantitative Analytics Dashboard** developed as part of the **Gemscap Quantitative Developer Intern Assignment**.

The application demonstrates a **mean-reversion based pairs trading strategy** using live cryptocurrency market data from the Binance Public API.

---

## 🚀 Features

- Live price data for BTCUSDT and ETHUSDT
- Selection of Y and X trading symbols
- Real-time **price spread** calculation
- Rolling mean & standard deviation
- **Z-score based mean reversion analysis**
- BUY / SELL / HOLD trading signals
- **Mean Reversion Half-Life** estimation
- Auto-refresh interval control
- Interactive Plotly charts (dark theme)
- Side-by-side visualization of:
  - Price Spread
  - Z-Score with threshold levels
- Real-time alerts based on signals
- CSV download of spread and z-score data

---

## 📈 Quantitative Logic

### Spread Calculation
Spread = Price(Y) − Price(X)

### Z-Score Calculation
Z-Score = (Spread − Rolling Mean) / Rolling Standard Deviation

### Trading Signals
Z > +2 → SELL Y / BUY X  
Z < −2 → BUY Y / SELL X  
Otherwise → HOLD

---

## ⏱ Mean Reversion Half-Life

The half-life represents how quickly the spread reverts to its mean.  
It is calculated using linear regression on lagged spread changes.

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Binance Public REST API

---

## ▶ How to Run

pip install -r requirements.txt  
streamlit run app.py

---

## 📤 Data Export

The dashboard allows downloading a CSV file containing:
- Timestamp
- Price Spread
- Z-Score

---

## ⚠ Disclaimer

This project is created for **educational and evaluation purposes only**.  
It does not constitute financial or investment advice.

---

## 👤 Author

**Vedant Keche**  
B.Tech – Electronics & Telecommunication Engineering  
Vishwakarma Institute of Technology, Pune
