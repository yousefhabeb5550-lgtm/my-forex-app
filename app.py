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
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🪙 **[قناص الذهب النهائي]**\n{message}", "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Gold Sniper Final Fix", page_icon="🪙")

# --- جلب السعر الفوري المباشر (أدق رمز متاح) ---
@st.cache_data(ttl=5) # تحديث فائق السرعة كل 5 ثوانٍ
def get_real_gold():
    try:
        # الرمز =X هو الأكثر تطابقاً مع منصات MetaTrader
        df = yf.download("XAUUSD=X", period="1d", interval="1m", progress=False)
        return df
    except: return pd.DataFrame()

df = get_real_gold()

st.title("🪙 قناص الذهب (التطابق التام)")

if not df.empty:
    # السعر المباشر
    current_price = round(float(df['Close'].iloc[-1]), 2)
    
    # حساب السيولة SMC
    recent_low = float(df['Low'].iloc[-20:-1].min())
    is_sweep = float(df['Low'].iloc[-1]) < recent_low and current_price > recent_low

    # عرض النتائج
    st.metric("سعر منصتك المباشر", f"${current_price}")
    
    # نظام المعايرة اليدوية الفورية (إذا وجدت فرق سنتات)
    st.sidebar.markdown("### ⚙️ ضبط دقيق")
    offset = st.sidebar.slider("تعديل السعر (سنتات):", -5.0, 5.0, 0.0)
    final_price = round(current_price + offset, 2)
    
    if offset != 0:
        st.subheader(f"✅ السعر المعاير: ${final_price}")

    if is_sweep:
        st.success("🎯 سحب سيولة مكتشف! السعر الآن كسر القاع وعاد بقوة.")
        send_alert(f"دخول شراء الآن!\nالسعر: {final_price}\nالهدف: {final_price + 1.50}")

else:
    st.error("جاري محاولة سحب السعر من القمر الصناعي... انتظر ثواني.")

# زر الاختبار
if st.sidebar.button("🚀 أرسل السعر لهاتفي"):
    send_alert(f"سعر الذهب الآن في الرادار: {current_price}\nهل تطابق مع المنصة؟")
                     
