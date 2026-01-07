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

# --- حساب RSI يدوياً ---
def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- واجهة المستخدم ---
st.set_page_config(page_title="Gorilla Multi-Radar", page_icon="🦍", layout="wide")

st.markdown("""
    <style>
    body { background-color: #0b0e14 !important; color: white; }
    .stApp { background-color: #0b0e14; }
    .pair-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; text-align: center; margin-bottom: 20px;
    }
    .price-tag { font-family: 'monospace'; font-size: 2.8rem; color: #00ff88; font-weight: bold; }
    .rsi-badge { padding: 4px 10px; border-radius: 8px; font-weight: bold; background: #0d1117; }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية مع زر الاختبار ---
with st.sidebar:
    st.title("🦍 Gorilla Control")
    if st.button("🚀 اختبار إرسال تليجرام"):
        send_gorilla_alert("TEST", "0.00", "✅ التوصيل شغال 100%!")
        st.success("تم الإرسال!")
    st.info("إذا توقفت الصفحة، قم بعمل Refresh للمتصفح.")

# --- محرك التحليل ---
def analyze_pair(symbol):
    try:
        # محاولة جلب البيانات بمهلة زمنية قصيرة لمنع التعليق
        df = yf.download(symbol, period="1d", interval="1m", progress=False, timeout=10)
        if df.empty or len(df) < 20: return None
        
        rsi_series = calculate_rsi(df['Close'])
        current_rsi = 50.0
        if not rsi_series.empty and not pd.isna(rsi_series.iloc[-1]):
            current_rsi = round(float(rsi_series.iloc[-1]), 2)
        
        ssl = float(df['Low'].iloc[-20:-1].min())
        current_low = float(df['Low'].iloc[-1])
        current_close = float(df['Close'].iloc[-1])
        
        # FVG logic
        fvg = float(df['Low'].iloc[-1]) > float(df['High'].iloc[-3])
        is_setup = current_low < ssl and current_close > ssl and fvg
        
        return {"price": round(current_close, 5), "ssl": round(ssl, 5), "rsi": current_rsi, "setup": is_setup}
    except:
        return None

# --- العرض الرئيسي ---
col1, col2 = st.columns(2)
pairs = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X"}

for col, (name, sym) in zip([col1, col2], pairs.items()):
    with col:
        res = analyze_pair(sym)
        if res:
            rsi_color = "#ff4b4b" if res['rsi'] > 70 else ("#00ff88" if res['rsi'] < 30 else "#8b949e")
            st.markdown(f"""
            <div class="pair-card">
                <small style="color:#8b949e">{name}</small>
                <div class="price-tag">{res['price']}</div>
                <div style="margin-top:10px">
                    <span style="color:#8b949e; font-size:0.8rem">RSI (14):</span>
                    <span class="rsi-badge" style="color: {rsi_color}">{res['rsi']}</span>
                </div>
                <hr style="border-color: #30363d;">
                <div class="row">
                    <div class="col-6"><small style="color:#8b949e">SSL</small><br><b>{res['ssl']}</b></div>
                    <div class="col-6"><small style="color:#8b949e">Status</small><br><b style="color: {'#00ff88' if res['setup'] else '#8b949e'}">{'ENTRY!' if res['setup'] else 'Scanning'}</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if res['setup']: send_gorilla_alert(name, res['price'], "Sweep + FVG! 🚀")
        else:
            st.warning(f"جاري محاولة جلب بيانات {name}...")

time.sleep(15)
st.rerun()
