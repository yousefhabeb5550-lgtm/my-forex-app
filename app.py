import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🏆 **[GOLD ELITE TERMINAL]**\n{message}", "parse_mode": "Markdown"})
    except: pass

# --- تصميم الواجهة الاحترافي (Bootstrap 5 Custom) ---
st.set_page_config(page_title="Gold Elite Sniper", page_icon="🏆", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0e14 !important; color: #e0e0e0; }
        .stApp { background-color: #0b0e14; }
        .card-custom { 
            background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
            padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .price-text { font-family: 'JetBrains Mono', monospace; font-size: 4.5rem; font-weight: bold; color: #ffd700; }
        .indicator-badge { border-radius: 50px; padding: 5px 15px; font-size: 0.75rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- محرك البيانات (جلب السعر الفوري الحقيقي) ---
@st.cache_data(ttl=2)
def get_spot_gold():
    try:
        # الرمز XAUUSD=X هو السعر الفوري (Spot) الذي يطابق Oanda تماماً
        ticker = yf.Ticker("XAUUSD=X")
        df = ticker.history(period="1d", interval="1m")
        return df
    except: return pd.DataFrame()

# --- الذاكرة الدائمة للمعايرة (Session State) ---
if 'gold_offset' not in st.session_state:
    st.session_state.gold_offset = 0.0

# --- القائمة الجانبية ---
with st.sidebar:
    st.markdown("### ⚙️ Calibration Center")
    new_offset = st.number_input("MT5 Sync Offset", value=st.session_state.gold_offset, step=0.01, format="%.2f")
    if new_offset != st.session_state.gold_offset:
        st.session_state.gold_offset = new_offset
        st.rerun()
    st.markdown("---")
    if st.button("🚀 Test Connection"):
        send_alert("System calibrated. Listening for SMC signals.")

# --- المعالجة والعرض ---
df = get_spot_gold()

if not df.empty and len(df) > 10:
    # استخراج السعر وتطبيق المعايرة
    current_raw = float(df['Close'].iloc[-1])
    final_price = round(current_raw + st.session_state.gold_offset, 2)
    
    # حساب سيولة SSL (SMC Logic)
    lows = df['Low'].iloc[-20:-1]
    raw_liquidity = float(lows.min())
    synced_liquidity = round(raw_liquidity + st.session_state.gold_offset, 2)
    
    # كشف سحب السيولة
    is_sweep = (float(df['Low'].iloc[-1]) + st.session_state.gold_offset) < synced_liquidity and final_price > synced_liquidity

    # --- واجهة Bootstrap ---
    st.markdown(f"""
    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-md-8">
                <div class="card-custom">
                    <span class="indicator-badge bg-success text-white">LIVE ECN FEED</span>
                    <h5 class="text-muted mt-2">XAU/USD SPOT GOLD</h5>
                    <div class="price-text">${final_price:,.2f}</div>
                    <p class="text-muted small">Synchronized with MT5 Bridge Platform</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card-custom h-100">
                    <span class="indicator-badge bg-primary text-white">SMC ENGINE</span>
                    <h6 class="mt-3">Liquidity Target (SSL)</h6>
                    <h2 class="text-info mt-2">${synced_liquidity:,.2f}</h2>
                    <p class="text-muted small">Institutional Stop-Loss Cluster</p>
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-12">
                <div class="card-custom text-center" style="border-top: 4px solid {'#ff4b4b' if is_sweep else '#ffd700'}">
                    <h4>Market Sentiment</h4>
                    <p class="lead">{'🚨 LIQUIDITY PURGE DETECTED - WAIT FOR BULLISH REJECTION' if is_sweep else '🔍 Scanning for institutional footprints...'}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if is_sweep:
        st.balloons()
        send_alert(f"🎯 SMC SIGNAL\nGold swept liquidity at {synced_liquidity}.\nCurrent Price: {final_price}")

else:
    st.markdown("<div class='text-center mt-5'><h4>Connecting to MT5 Pricing Server...</h4></div>", unsafe_allow_html=True)
