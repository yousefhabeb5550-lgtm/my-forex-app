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
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🪙 **[قناص الذهب المطور]**\n{message}", "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Gold Sniper Pro", page_icon="🪙")

# --- جلب البيانات (حل مشكلة التطابق) ---
@st.cache_data(ttl=15)
def get_live_gold():
    try:
        # الرمز =P يعطي السعر الفوري اللحظي الأكثر دقة
        data = yf.download("XAUUSD=P", period="1d", interval="1m", progress=False)
        if data.empty:
            data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        return data
    except:
        return pd.DataFrame()

df = get_live_gold()

st.title("🪙 رادار الذهب (مطابق لمنصتك)")

if not df.empty:
    # الحصول على السعر الحالي
    current_price = round(float(df['Close'].iloc[-1]), 2)
    
    # حساب السيولة (SMC)
    recent_low = float(df['Low'].iloc[-20:-1].min())
    is_sweep = float(df['Low'].iloc[-1]) < recent_low and current_price > recent_low
    
    # عرض السعر الكبير
    st.metric("سعر الذهب الحالي (XAU/USD)", f"${current_price}")
    
    # مقارنة بصرية للمستخدم
    st.info(f"📍 دعم السيولة القريب: {recent_low}")

    if is_sweep:
        st.success("🎯 سحب سيولة (Sweep) مكتشف الآن!")
        send_alert(f"إشارة SMC مؤكدة!\nالسعر: {current_price}\nالستوب: {current_price - 0.50}")

    # زر الاختبار في الجنب
    if st.sidebar.button("🚀 اختبار تليجرام"):
        send_alert(f"منصة الذهب تعمل! السعر اللحظي: {current_price}")
        st.sidebar.success("تم إرسال الاختبار!")
else:
    st.error("⚠️ فشل جلب البيانات. يرجى إعادة تحميل الصفحة بعد ثوانٍ.")
