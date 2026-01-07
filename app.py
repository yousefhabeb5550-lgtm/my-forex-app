import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import time

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🦍 [GBP/USD] {msg}"}, timeout=5)
    except: pass

# --- واجهة الغوريلا الاحترافية ---
st.set_page_config(page_title="GBP Sniper", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .main-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 20px; 
        padding: 40px; text-align: center; margin-top: 20px;
    }
    .price { font-size: 5rem; color: #58a6ff; font-weight: bold; font-family: 'Courier New'; }
    </style>
""", unsafe_allow_html=True)

st.title("🦍 رادار قناص الباوند")

# --- جلب وتحليل البيانات ---
try:
    ticker = yf.Ticker("GBPUSD=X")
    # جلب بيانات كافية لحساب RSI والسيولة
    df = ticker.history(period="1d", interval="1m")
    
    if not df.empty:
        current_price = float(df['Close'].iloc[-1])
        # تحديد أدنى مستوى في آخر 20 دقيقة كسيولة (SSL)
        ssl_level = float(df['Low'].iloc[-20:-1].min())
        
        # شرط الدخول (SMC): كسر السيولة ثم العودة فوقها
        is_setup = df['Low'].iloc[-1] < ssl_level and current_price > ssl_level

        st.markdown(f"""
            <div class="main-card">
                <h3 style="color:#8b949e">LIVE GBP / USD</h3>
                <div class="price">{current_price:.5f}</div>
                <p style="font-size:1.2rem; color:#8b949e">Target Liquidity: {ssl_level:.5f}</p>
                <hr style="border-color:#333">
                <h2 style="color: {'#00ff88' if is_setup else '#8b949e'}">
                    {'🚨 ENTRY DETECTED!' if is_setup else '🔍 Scanning...'}
                </h2>
            </div>
        """, unsafe_allow_html=True)

        if is_setup:
            send_telegram(f"🚨 فرصة قنص! السعر: {current_price:.5f}")
            st.balloons()

except Exception as e:
    st.info("🔄 جاري الاتصال بمزود البيانات العالمي...")

# زر اختبار يدوي في الجانب
with st.sidebar:
    if st.button("🚀 اختبار تليجرام"):
        send_telegram("✅ التوصيل ممتاز!")
        st.success("تم الإرسال")

# تحديث تلقائي كل 15 ثانية
time.sleep(15)
st.rerun()
