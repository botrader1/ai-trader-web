import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime
from binance.client import Client

st.set_page_config(layout="wide")
st.title("📊 AI Trading Dashboard")

# Binance API Section
st.subheader("🔐 Connect Your Binance Account")
api_key = st.text_input("API Key")
api_secret = st.text_input("API Secret", type="password")
use_testnet = st.checkbox("Use Testnet")

if api_key and api_secret:
    try:
        client = Client(api_key, api_secret)
        if use_testnet:
            client.API_URL = 'https://testnet.binance.vision/api'
        account_info = client.get_account()
        balances = account_info['balances']
        non_zero = [b for b in balances if float(b['free']) > 0 or float(b['locked']) > 0]
        st.success("✅ Connected to Binance!")
        st.dataframe(non_zero)
    except Exception as e:
        st.error(f"❌ Connection error: {e}")

# Simulated portfolio data
st.subheader("📈 Portfolio Value Over Time")
dates = pd.date_range(end=datetime.datetime.today(), periods=30).to_pydatetime().tolist()
values = np.cumsum(np.random.randn(30) * 100)
df = pd.DataFrame({"date": dates, "portfolio_value": values})
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['portfolio_value'], mode='lines+markers', name='Portfolio Value'))
fig.update_layout(xaxis_title='Date', yaxis_title='Value (USD)', height=400)
st.plotly_chart(fig, use_container_width=True)
