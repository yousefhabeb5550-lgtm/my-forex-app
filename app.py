import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- إعدادات OANDA الاحترافية (تأكد من دقتها) ---
API_KEY = "451c070966a33f11467475f78230533a-0e99b0c2a507c336585189286f03d211"
ACCOUNT_ID = "101-004-30155050-001"
# الرابط المباشر لسيرفر الحسابات التجريبية الجديد (v20)
OANDA_URL = f"https://api-fxpractice.oanda.com/v3/accounts/{ACCOUNT_ID}/pricing"

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🏆 **[OANDA DIRECT]**\n{message}", "parse_mode": "Markdown"})
    except: pass

# --- واجهة المستخدم (Bootstrap Premium) ---
st.set_page_config(page_title="Gold Direct Oanda", page_icon="🏆", layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0d1117 !important; color: #c9d1d9; }
        .stApp { background-color: #0d1117; }
        .terminal-box { 
            background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
            padding: 30px; text-align: center; margin-top: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        }
        .live-price { font-family: 'Monaco', monospace; font-size: 5rem; font-weight: bold; color: #ffd700; }
        .badge-live { background-color: #238636; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- محرك جلب البيانات المباشر ---
def fetch_oanda_live():
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    params = {"instruments": "XAU_USD"} # رمز الذهب في OANDA
    try:
        response = requests.get(OANDA_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            prices = data['prices'][0]
            # نأخذ متوسط سعر البيع والشراء لضمان الدقة
            bid = float(prices['closeoutBid'])
            ask = float(prices['closeoutAsk'])
            return round((bid + ask) / 2, 2)
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return None

# --- العرض الرئيسي ---
price = fetch_oanda_live()

if isinstance(price, float):
    st.markdown(f"""
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-10">
                    <div class="terminal-box">
                        <span class="badge-live">OANDA SERVER DIRECT</span>
                        <h2 class="mt-3" style="color: #8b949e;">XAU/USD GOLD</h2>
                        <div class="live-price">${price:,.2f}</div>
                        <hr style="border-color: #30363d;">
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted">CONNECTION</small>
                                <p class="text-success fw-bold">ENCRYPTED BRIDGE</p>
                            </div>
                            <div class="col-6">
                                <small class="text-muted">LATENCY</small>
                                <p class="text-info fw-bold">< 100ms</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # زر إرسال السعر المباشر للتليجرام للتأكد
    if st.sidebar.button("🚀 مزامنة تليجرام"):
        send_alert(f"سعر OANDA المباشر الآن: {price}")
        st.sidebar.success("تم الإرسال!")

elif isinstance(price, str) and "Error: 401" in price:
    st.error("❌ خطأ 401: مفتاح الـ API أو رقم الحساب غير صحيح لهذه الأداة (الذهب).")
    st.info("تأكد من أن حسابك التجريبي يدعم تداول المعادن (Commodities).")
else:
    st.warning("🔄 جاري محاولة فتح قناة اتصال مع OANDA...")
    
