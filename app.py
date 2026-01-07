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
        text = f"🦍 **[GORILLA ALERT: {pair}]**\n💰 السعر: {price}\n📝 الحالة: {msg}"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except: pass

# --- تصميم الواجهة (Custom Bootstrap Grid) ---
st.set_page_config(page_title="Gorilla Multi-Radar", page_icon="🦍", layout="wide")
st.markdown("""
    <style>
    body { background-color: #0b0e14 !important; color: white; }
    .stApp { background-color: #0b0e14; }
    .pair-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; text-align: center; margin-bottom: 20px;
    }
    .price-tag { font-family: 'JetBrains Mono', monospace; font-size: 2.5rem; color: #00ff88; font-weight: bold; }
    .label { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- محرك التحليل الفني (SMC Logic) ---
def analyze_pair(symbol):
    df = yf.download(symbol, period="1d", interval="1m", progress=False)
    if df.empty or len(df) < 25: return None
    
    # 1. تحديد السيولة (SSL) - قاع آخر 20 دقيقة
    ssl = float(df['Low'].iloc[-20:-1].min())
    current_low = float(df['Low'].iloc[-1])
    current_close = float(df['Close'].iloc[-1])
    
    # 2. كشف الـ FVG (الاندفاع المؤسسي)
    # فجوة بين شمعة 1 (قبل السابقة) وشمعة 3 (الحالية)
    prev_high = float(df['High'].iloc[-3])
    curr_low = float(df['Low'].iloc[-1])
    fvg_detected = curr_low > prev_high
    
    # 3. شرط الغوريلا (Sweep + Rejection + FVG)
    is_setup = current_low < ssl and current_close > ssl and fvg_detected
    
    return {
        "price": round(current_close, 5),
        "ssl": round(ssl, 5),
        "setup": is_setup
    }

# --- العرض الرئيسي ---
st.title("🦍 Gorilla Multi-Pair Sniper")
st.write(f"🔄 **Last Update:** {time.strftime('%H:%M:%S')}")

col1, col2 = st.columns(2)

pairs = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"}

# عرض اليورو
with col1:
    res = analyze_pair(pairs["EUR/USD"])
    if res:
        st.markdown(f"""
        <div class="pair-card">
            <div class="label">EUR / USD</div>
            <div class="price-tag">{res['price']}</div>
            <hr style="border-color: #30363d;">
            <div class="row">
                <div class="col-6"><small>Liquidity (SSL)</small><br><b>{res['ssl']}</b></div>
                <div class="col-6"><small>Status</small><br><b style="color: {'#00ff88' if res['setup'] else '#8b949e'}">{'ENTRY!' if res['setup'] else 'Scanning'}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if res['setup']:
            st.balloons()
            send_gorilla_alert("EUR/USD", res['price'], "Sweep + FVG Confirmed! 🚀")

# عرض الباوند
with col2:
    res = analyze_pair(pairs["GBP/USD"])
    if res:
        st.markdown(f"""
        <div class="pair-card">
            <div class="label">GBP / USD</div>
            <div class="price-tag" style="color: #58a6ff;">{res['price']}</div>
            <hr style="border-color: #30363d;">
            <div class="row">
                <div class="col-6"><small>Liquidity (SSL)</small><br><b>{res['ssl']}</b></div>
                <div class="col-6"><small>Status</small><br><b style="color: {'#00ff88' if res['setup'] else '#8b949e'}">{'ENTRY!' if res['setup'] else 'Scanning'}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if res['setup']:
            st.balloons()
            send_gorilla_alert("GBP/USD", res['price'], "Sweep + FVG Confirmed! 🚀")

# تحديث تلقائي
time.sleep(15)
st.rerun()

# --- إضافة زر الاختبار في القائمة الجانبية ---
with st.sidebar:
    st.markdown("### 🧪 اختبار الاتصال")
    if st.button("🚀 إرسال رسالة تجريبية"):
        test_msg = "✅ نظام الغوريلا متصل بنجاح! الرادار يعمل الآن ويراقب اليورو والباوند."
        send_gorilla_alert("SYSTEM CHECK", "N/A", test_msg)
        st.success("تم إرسال الرسالة إلى تليجرام!")
        
