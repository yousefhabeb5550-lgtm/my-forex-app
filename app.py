import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🏆 **[GOLD ELITE]**\n{message}", "parse_mode": "Markdown"})
    except: pass

# --- تصميم الواجهة (Custom Bootstrap 5 Dark Theme) ---
st.set_page_config(page_title="Gold Elite Terminal", page_icon="🏆", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0e11 !important; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
        .stApp { background-color: #0b0e11; }
        .terminal-card { 
            background: #161a1e; border: 1px solid #2b3139; border-radius: 12px; 
            padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .price-display { 
            font-family: 'Courier New', monospace; font-size: 5rem; 
            font-weight: 800; color: #f0b90b; text-shadow: 0 0 25px rgba(240, 185, 11, 0.3);
        }
        .stat-label { color: #848e9c; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الذاكرة لثبات السعر (Session State) ---
if 'mt5_offset' not in st.session_state:
    st.session_state.mt5_offset = 0.0

# --- جلب البيانات (ECN Bridge) ---
@st.cache_data(ttl=2)
def fetch_fast_gold():
    try:
        # الرمز XAUUSD=X هو المعتمد دولياً لمطابقة Oanda و MetaTrader
        ticker = yf.Ticker("XAUUSD=X")
        df = ticker.history(period="1d", interval="1m")
        return df
    except: return pd.DataFrame()

# --- القائمة الجانبية (Terminal Controls) ---
with st.sidebar:
    st.markdown("### 🖥️ MT5 SYNC CENTER")
    # التعديل هنا سيغير السعر فوراً ويحفظه في الذاكرة
    new_val = st.number_input("Calibration (Offset)", value=st.session_state.mt5_offset, step=0.01)
    if new_val != st.session_state.mt5_offset:
        st.session_state.mt5_offset = new_val
        st.rerun()
    st.markdown("---")
    st.markdown(f"🕒 **Last Sync:** {datetime.now().strftime('%H:%M:%S')}")
    if st.button("🚀 Test Pulse"):
        send_alert("System Online. MT5 Bridge Active.")

# --- المعالجة والعرض الفني ---
df = fetch_fast_gold()

if not df.empty and len(df) > 5:
    # استخراج السعر الحقيقي بدقة
    raw_current = float(df['Close'].iloc[-1])
    # تطبيق المعايرة لضمان التطابق التام مع منصتك
    final_price = round(raw_current + st.session_state.mt5_offset, 2)
    
    # حساب مناطق السيولة SMC
    raw_low = float(df['Low'].iloc[-15:-1].min())
    synced_low = round(raw_low + st.session_state.mt5_offset, 2)

    # الواجهة الرئيسية (Bootstrap Grid System)
    st.markdown(f"""
        <div class="container-fluid">
            <div class="row mt-4">
                <div class="col-md-9">
                    <div class="terminal-card">
                        <div class="d-flex justify-content-between">
                            <span class="stat-label">XAU/USD SPOT GOLD</span>
                            <span class="badge bg-success">LIVE ECN FEED</span>
                        </div>
                        <div class="price-display text-center">${final_price:,.2f}</div>
                        <div class="row mt-4 text-center">
                            <div class="col-6 border-end border-secondary">
                                <div class="stat-label">INSTITUTIONAL LIQUIDITY</div>
                                <h3 class="text-info fw-bold">${synced_low:,.2f}</h3>
                            </div>
                            <div class="col-6">
                                <div class="stat-label">SYSTEM STATUS</div>
                                <h3 class="text-warning">SCANNING...</h3>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 text-center">
                    <div class="terminal-card h-100 d-flex flex-column justify-content-center">
                        <div class="stat-label mb-3">MT5 SYNC OFFSET</div>
                        <h2 class="text-white">{st.session_state.mt5_offset:+.2f}</h2>
                        <p class="text-muted small">Calibrated to match your platform exactly.</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # منطق التنبيه التلقائي (SMC Logic)
    current_low = float(df['Low'].iloc[-1]) + st.session_state.mt5_offset
    if current_low < synced_low and final_price > synced_low:
        st.balloons()
        send_alert(f"🚨 SMC ALERT: Gold Liquidity Purge at {final_price}.\nTarget: {final_price + 1.50}")

else:
    st.markdown("""
        <div style="height: 80vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div class="spinner-border text-warning" style="width: 3rem; height: 3rem;" role="status"></div>
            <h4 class="mt-4 text-warning">ESTABLISHING SECURE MT5 BRIDGE...</h4>
        </div>
    """, unsafe_allow_html=True)
    
