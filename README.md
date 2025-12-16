# Gemscap Quantitative Analytics Dashboard

This project is a real-time quantitative analytics dashboard built as part of the Gemscap Quantitative Developer Intern assignment.

## Features
- Live BTCUSDT price fetched from Binance public API
- Tick-by-tick return calculation
- Z-score based mean reversion analysis
- Trading signal: BUY / SELL / HOLD
- Interactive charts using Plotly

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- Binance Public API

## Quantitative Logic
- Return = Percentage change in price
- Z-score = (Price − Rolling Mean) / Rolling Standard Deviation
- Trading Signal:
  - BUY → Z-score < -2
  - SELL → Z-score > 2
  - HOLD → Otherwise

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
