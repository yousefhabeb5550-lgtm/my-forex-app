import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- إعدادات الوصول (Golden) ---
API_KEY = "451c070966a33f11467475f78230533a-0e99b0c2a507c336585189286f03d211"
ACCOUNT_ID = "101-004-30155050-001"
OANDA_URL = f"https://api-fxpractice.oanda.com/v3/accounts/{ACCOUNT_ID}/instruments/XAU_USD/candles"

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🪙 **[قناص الذهب - OANDA]**\n{message}", "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Gold Sniper Oanda", page_icon="🪙")

# --- جلب البيانات من Oanda ---
def get_oanda_gold():
    params = {"count": 50, "granularity": "M1"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(OANDA_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()['candles']
            prices = []
            for candle in data:
                prices.append({
                    'time': candle['time'],
                    'close': float(candle['mid']['c']),
                    'low': float(candle['mid']['l']),
                    'high': float(candle['mid']['h'])
                })
            return pd.DataFrame(prices)
    except:
        return pd.DataFrame()

df = get_oanda_gold()

st.title("🪙 رادار الذهب (بيانات OANDA الدقيقة)")

if df is not None and not df.empty:
    current_price = df['close'].iloc[-1]
    
    # حساب SMC بناءً على سعر Oanda
    recent_low = df['low'].iloc[-20:-1].min()
    is_sweep = df['low'].iloc[-1] < recent_low and current_price > recent_low
    
    # عرض السعر المطابق للمنصة
    st.metric("سعر XAU/USD (Oanda)", f"${current_price:.2f}")
    
    st.write(f"🔍 دعم السيولة الحالي: {recent_low:.2f}")

    if is_sweep:
        st.success("🎯 سحب سيولة مكتشف! السعر الآن مطابق لمنصتك تماماً.")
        if 'last_oanda_alert' not in st.session_state or st.session_state.last_oanda_alert != current_price:
            send_alert(f"فرصة SMC مكتشفة!\nسعر الدخول: {current_price}\nالستوب والهدف مطابقة لمنصتك.")
            st.session_state.last_oanda_alert = current_price
else:
    st.error("⚠️ خطأ في الاتصال بـ Oanda. تأكد من الـ API Key.")

# زر الاختبار
if st.sidebar.button("🚀 اختبار السعر"):
    send_alert(f"فحص السعر: {current_price} - قارنه بمنصتك الآن!")
        
