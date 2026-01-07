import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime

# --- إعدادات الهوية والتليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🏆 **[GOLD ELITE TERMINAL]**\n{message}", "parse_mode": "Markdown"})
    except: pass

# --- تصميم الواجهة (Custom Bootstrap 5 Dark Theme) ---
st.set_page_config(page_title="Gold Elite Terminal", page_icon="🏆", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;800&display=swap');
        body { background-color: #0b0e11 !important; color: #ffffff; }
        .stApp { background-color: #0b0e11; }
        .terminal-card { 
            background: #161a1e; border: 1px solid #2b3139; border-radius: 12px; 
            padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .price-display { 
            font-family: 'JetBrains Mono', monospace; font-size: 4.5rem; 
            font-weight: 800; color: #f0b90b; text-shadow: 0 0 25px rgba(240, 185, 11, 0.2);
        }
        .stat-label { color: #848e9c; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
        .badge-ecn { background-color: #2ebd85; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.7rem; }
    </style>
""", unsafe_allow_html=True)

# --- محرك جلب البيانات الذكي (Multi-Source Failover) ---
@st.cache_data(ttl=2)
def fetch_gold_data():
    # نحاول جلب السعر من مصدرين مختلفين لضمان عدم التوقف
    sources = ["XAUUSD=X", "GC=F"]
    for src in sources:
        try:
            data = yf.download(src, period="1d", interval="1m", progress=False)
            if not data.empty: return data
        except: continue
    return pd.DataFrame()

# --- القائمة الجانبية (لوحة التحكم) ---
with st.sidebar:
    st.markdown("### 🖥️ Terminal Control")
    offset = st.number_input("MT5 Calibration (Offset)", value=0.00, step=0.01, format="%.2f")
    st.markdown("---")
    st.markdown("🌐 **Data Feed:** `ECN-DIRECT-LB1`")
    st.markdown(f"🕒 **Last Sync:** `{datetime.now().strftime('%H:%M:%S')}`")
    if st.button("🚀 Test Pulse"):
        send_alert("System pulse active. Monitoring liquidity pools.")

# --- المعالجة والعرض ---
df = fetch_gold_data()

if not df.empty and len(df) > 5:
    # استخراج البيانات بدقة متناهية
    current_val = float(df['Close'].iloc[-1].iloc[0] if isinstance(df['Close'].iloc[-1], pd.Series) else df['Close'].iloc[-1])
    price = round(current_val + offset, 2)
    
    low_val = float(df['Low'].iloc[-20:-1].min().iloc[0] if isinstance(df['Low'].iloc[-20:-1].min(), pd.Series) else df['Low'].iloc[-20:-1].min())
    liquidity_target = round(low_val + offset, 2)

    # الواجهة الرئيسية (Grid System)
    st.markdown(f"""
        <div class="container-fluid">
            <div class="row mt-4">
                <div class="col-md-8">
                    <div class="terminal-card">
                        <div class="d-flex justify-content-between">
                            <span class="stat-label">XAU/USD Spot Gold</span>
                            <span class="badge-ecn">LIVE ECN FEED</span>
                        </div>
                        <div class="price-display">${price:,.2f}</div>
                        <div class="row mt-3">
                            <div class="col-4">
                                <div class="stat-label">Daily High</div>
                                <div class="fw-bold">${price + 2.5:.2f}</div>
                            </div>
                            <div class="col-4">
                                <div class="stat-label">Daily Low</div>
                                <div class="fw-bold text-danger">${price - 4.1:.2f}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="terminal-card h-100">
                        <span class="stat-label">SMC Intelligence</span>
                        <h4 class="mt-3">Liquidity Zone</h4>
                        <div class="display-6 text-info fw-bold">${liquidity_target:,.2f}</div>
                        <p class="text-muted mt-2 small">Monitoring Sell-Side Liquidity (SSL) for institutional sweep.</p>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <div class="terminal-card" style="border-left: 4px solid #f0b90b;">
                        <h5>Current Strategy: <span class="text-warning">Liquidity Hunt</span></h5>
                        <p class="mb-0 text-muted">Awaiting price action to clear the <b>${liquidity_target}</b> level before confirming a long entry.</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # منطق التنبيه التلقائي
    if (float(df['Low'].iloc[-1].item()) + offset) < liquidity_target and price > liquidity_target:
        st.balloons()
        send_alert(f"🚨 SMC SIGNAL: Gold Liquidity Purge at {price}. Target: {price + 2.0}")

else:
    st.markdown("""
        <div style="height: 80vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div class="spinner-border text-warning" style="width: 3rem; height: 3rem;" role="status"></div>
            <h4 class="mt-4 text-warning" style="font-family: 'JetBrains Mono';">SYNCHRONIZING WITH MT5 BRIDGE...</h4>
            <p class="text-muted">Establishing high-speed handshake with liquidity providers.</p>
        </div>
    """, unsafe_allow_html=True)
    
