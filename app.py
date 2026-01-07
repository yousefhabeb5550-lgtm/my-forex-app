import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_gorilla_alert(pair, price, msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        text = f"🦍 **[GORILLA ALERT: {pair}]**\n💰 Price: {price}\n📝 Status: {msg}"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "timeout": 5})
    except: pass

# --- واجهة المستخدم ---
st.set_page_config(page_title="Multi-Radar Pro", page_icon="🦍", layout="wide")

st.markdown("""
    <style>
    body { background-color: #0b0e14 !important; color: white; }
    .stApp { background-color: #0b0e14; }
    .pair-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; text-align: center; margin-bottom: 20px;
    }
    .price-tag { font-family: 'monospace'; font-size: 2.5rem; color: #00ff88; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- محرك التحليل ---
def analyze_pair(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 20: return None
        
        price = round(df['Close'].iloc[-1], 5)
        ssl = round(df['Low'].iloc[-20:-1].min(), 5)
        
        # SMC Simple Logic: Sweep + Rejection
        setup = df['Low'].iloc[-1] < ssl and df['Close'].iloc[-1] > ssl
        
        return {"price": price, "ssl": ssl, "setup": setup}
    except: return None

# --- العرض الرئيسي ---
st.title("🦍 رادار الغوريلا المزدوج")

col1, col2 = st.columns(2)
pairs = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"}

with col1:
    res1 = analyze_pair(pairs["EUR/USD"])
    if res1:
        st.markdown(f"""
        <div class="pair-card">
            <h3>EUR/USD</h3>
            <div class="price-tag">{res1['price']}</div>
            <p>Liquidity (SSL): {res1['ssl']}</p>
            <h4 style="color: {'#00ff88' if res1['setup'] else '#8b949e'}">
                {'🚨 ENTRY DETECTED' if res1['setup'] else '🔍 Scanning...'}
            </h4>
        </div>
        """, unsafe_allow_html=True)

with col2:
    res2 = analyze_pair(pairs["GBP/USD"])
    if res2:
        st.markdown(f"""
        <div class="pair-card">
            <h3>GBP/USD</h3>
            <div class="price-tag" style="color:#58a6ff">{res2['price']}</div>
            <p>Liquidity (SSL): {res2['ssl']}</p>
            <h4 style="color: {'#00ff88' if res2['setup'] else '#8b949e'}">
                {'🚨 ENTRY DETECTED' if res2['setup'] else '🔍 Scanning...'}
            </h4>
        </div>
        """, unsafe_allow_html=True)

# التحديث التلقائي
time.sleep(20)
st.rerun()
