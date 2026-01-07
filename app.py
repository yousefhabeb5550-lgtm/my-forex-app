import streamlit as st
import yfinance as yf
import time
import requests

# إعدادات التليجرام
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=2)
    except: pass

st.set_page_config(page_title="GBP Sniper", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; text-align: center; }
    .price-box { font-size: 5rem; color: #58a6ff; font-weight: bold; margin: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🦍 رادار الباوند السريع")

try:
    # جلب أسرع نسخة للسعر
    ticker = yf.Ticker("GBPUSD=X")
    price = ticker.fast_info['last_price']
    
    st.markdown(f'<div class="price-box">{price:.5f}</div>', unsafe_allow_html=True)
    st.success("✅ الرادار متصل ويعمل الآن")
    
    if st.button("🚀 اختبار تليجرام سريع"):
        send_msg("✅ البوت شغال يا شريكي!")
        st.toast("تم الإرسال!")

except Exception as e:
    st.warning("🔄 السيرفر يحاول الاتصال بالأسعار العالمية...")

# تحديث كل 10 ثواني
time.sleep(10)
st.rerun()
