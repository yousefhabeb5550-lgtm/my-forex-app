import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- إعدادات الواجهة (Professional Dark Bootstrap) ---
st.set_page_config(page_title="Gold Sniper Terminal", page_icon="🏆", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0e11 !important; color: #ffffff; }
        .stApp { background-color: #0b0e11; }
        .terminal-card { 
            background: #161a1e; border: 1px solid #30363d; border-radius: 15px; 
            padding: 40px; margin-top: 30px; text-align: center;
            box-shadow: 0 15px 50px rgba(0,0,0,0.7);
        }
        .price-text { font-family: 'Courier New', monospace; font-size: 6rem; font-weight: 900; color: #f0b90b; }
        .sync-badge { background: #238636; color: white; padding: 5px 15px; border-radius: 50px; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- إدارة الذاكرة (لحل مشكلة القفز السعري) ---
if 'calibration' not in st.session_state:
    st.session_state.calibration = 0.0

# --- محرك البيانات الفولاذي (Anti-Crash Engine) ---
def get_gold_price():
    # محاولة جلب البيانات 3 مرات قبل الاستسلام
    for _ in range(3):
        try:
            # XAUUSD=X هو الرمز الأكثر استقراراً في العالم حالياً
            data = yf.download("XAUUSD=X", period="1d", interval="1m", progress=False)
            if not data.empty:
                return data
        except:
            time.sleep(1) # انتظر ثانية وحاول مجدداً
    return None

# --- التحكم الجانبي ---
with st.sidebar:
    st.header("⚙️ معايرة المنصة")
    st.info("اضبط هذا الرقم مرة واحدة ليطابق ميتاتريدر تماماً.")
    new_offset = st.number_input("الفرق (Offset)", value=st.session_state.calibration, step=0.01)
    if new_offset != st.session_state.calibration:
        st.session_state.calibration = new_offset
        st.rerun()

# --- العرض الرئيسي ---
data = get_gold_price()

if data is not None:
    # معالجة السعر وضمان أنه رقم
    raw_val = float(data['Close'].iloc[-1])
    final_price = round(raw_val + st.session_state.calibration, 2)
    
    # حساب السيولة
    low_val = float(data['Low'].iloc[-10:-1].min())
    liquidity = round(low_val + st.session_state.calibration, 2)

    st.markdown(f"""
        <div class="container">
            <div class="terminal-card">
                <span class="sync-badge">SERVER: CONNECTED</span>
                <h4 class="text-muted mt-4">XAU/USD SPOT</h4>
                <div class="price-text">${final_price:,.2f}</div>
                <div class="row mt-5">
                    <div class="col-6 border-end border-secondary">
                        <small class="text-muted">INSTITUTIONAL SUPPORT</small>
                        <h2 class="text-info">${liquidity:,.2f}</h2>
                    </div>
                    <div class="col-6">
                        <small class="text-muted">MT5 OFFSET</small>
                        <h2 class="text-warning">{st.session_state.calibration:+.2f}</h2>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # تحديث تلقائي كل 5 ثوانٍ
    time.sleep(5)
    st.rerun()
else:
    # واجهة انتظار احترافية بدلاً من الخطأ الأحمر
    st.markdown("""
        <div class="text-center" style="margin-top: 200px;">
            <div class="spinner-border text-warning" role="status" style="width: 4rem; height: 4rem;"></div>
            <h2 class="mt-4">جاري إعادة الاتصال بمزود الأسعار...</h2>
            <p class="text-muted">يرجى التأكد من استقرار الإنترنت لديك.</p>
        </div>
    """, unsafe_allow_html=True)
    
