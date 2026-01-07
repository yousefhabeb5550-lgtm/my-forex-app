import streamlit as st
import yfinance as yf
import pandas as pd
import requests

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🏆 **[GOLD RADAR]**\n{message}", "parse_mode": "Markdown"})
    except: pass

# --- واجهة المستخدم الاحترافية ---
st.set_page_config(page_title="Gold Elite Sniper", page_icon="🏆", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0e11 !important; color: #e0e0e0; }
        .stApp { background-color: #0b0e11; }
        .terminal-card { 
            background: #161a1e; border: 1px solid #2b3139; border-radius: 15px; 
            padding: 30px; margin-top: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        .price-big { font-family: 'JetBrains Mono', monospace; font-size: 5.5rem; font-weight: 800; color: #f0b90b; }
        .status-tag { background: #2ebd85; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- نظام الذاكرة المستقرة (Session State) ---
# هذا الجزء يضمن أن السعر لن يقفز للأصل عند التحديث
if 'calib' not in st.session_state:
    st.session_state.calib = 0.09 # فرق السنتات الذي لاحظناه في صورتك

# --- جلب البيانات ---
@st.cache_data(ttl=1)
def get_stable_data():
    try:
        # الرمز XAUUSD=X هو الأدق لتطابق Oanda و MetaTrader
        df = yf.download("XAUUSD=X", period="1d", interval="1m", progress=False)
        return df
    except: return pd.DataFrame()

# --- لوحة التحكم الجانبية ---
with st.sidebar:
    st.markdown("### ⚙️ إعدادات المزامنة")
    new_calib = st.number_input("معايرة السعر (Offset)", value=st.session_state.calib, step=0.01, format="%.2f")
    if new_calib != st.session_state.calib:
        st.session_state.calib = new_calib
        st.rerun()
    st.write("---")
    if st.button("🚀 اختبار التليجرام"):
        send_alert("الرادار متصل وجاهز للقنص.")

# --- المعالجة والعرض ---
df = get_stable_data()

if not df.empty and len(df) > 5:
    # استخراج السعر كمصفوفة نظيفة لتجنب ValueError
    raw_current = float(df['Close'].iloc[-1].item())
    current_price = round(raw_current + st.session_state.calib, 2)
    
    # حساب سيولة الـ SMC
    raw_low = float(df['Low'].iloc[-15:-1].min().item())
    liquidity_target = round(raw_low + st.session_state.calib, 2)

    # عرض الواجهة (Grid System)
    st.markdown(f"""
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="terminal-card text-center">
                        <span class="status-tag">REAL-TIME SYNC</span>
                        <h2 class="text-muted mt-3">XAU/USD GOLD SPOT</h2>
                        <div class="price-big">${current_price:,.2f}</div>
                        <div class="row mt-4 justify-content-center">
                            <div class="col-md-4">
                                <small class="text-muted d-block">INSTITUTIONAL SUPPORT</small>
                                <h3 class="text-info">${liquidity_target:,.2f}</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # منطق القنص
    current_low_full = float(df['Low'].iloc[-1].item()) + st.session_state.calib
    if current_low_full < liquidity_target and current_price > liquidity_target:
        st.balloons()
        send_alert(f"🎯 إشارة قنص ذهب!\nالسعر: {current_price}\nالهدف: {current_price + 1.80}")

else:
    st.markdown("<h4 class='text-center mt-5 text-warning'>جاري استعادة الاتصال بمزودي السيولة...</h4>", unsafe_allow_html=True)
    
