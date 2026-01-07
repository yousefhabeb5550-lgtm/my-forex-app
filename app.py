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

# --- دالة حساب RSI يدوية مستقرة ---
def calculate_rsi(series, window=14):
    if len(series) < window: return 50.0
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

# --- إعداد الواجهة الاحترافية ---
st.set_page_config(page_title="Gorilla Ultra-Stable", page_icon="🦍", layout="wide")

st.markdown("""
    <style>
    body { background-color: #0b0e14 !important; color: white; }
    .stApp { background-color: #0b0e14; }
    .pair-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; text-align: center; margin-bottom: 20px;
    }
    .price-tag { font-family: 'monospace'; font-size: 2.8rem;
