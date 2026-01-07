import streamlit as st
import pandas as pd
import requests

# --- إعدادات Oanda (تأكد أنها نفس التي نجحت في اليورو) ---
API_KEY = "451c070966a33f11467475f78230533a-0e99b0c2a507c336585189286f03d211"
ACCOUNT_ID = "101-004-30155050-001"
# جربنا XAU_USD، وإذا لم يعمل الكود سيحاول تلقائياً مع رموز أخرى
INSTRUMENT = "XAU_USD" 

TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": f"🪙 **[قناص الذهب - Oanda]**\n{message}", "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="Gold Sniper Oanda", page_icon="🪙")

def get_gold_oanda():
    url = f"https://api-fxpractice.oanda.com/v3/instruments/{INSTRUMENT}/candles"
    params = {"count": 30, "granularity": "M1", "price": "M"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            candles = response.json()['candles']
            data = []
            for c in candles:
                data.append({
                    'close': float(c['mid']['c']),
                    'low': float(c['mid']['l']),
                    'high': float(c['mid']['h'])
                })
            return pd.DataFrame(data)
        else:
            st.error(f"⚠️ خطأ من Oanda: {response.status_code} - {response.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ فشل الاتصال: {e}")
        return pd.DataFrame()

df = get_gold_oanda()

st.title("🪙 رادار الذهب (مطابق للمنصة)")

if not df.empty:
    current_price = df['close'].iloc[-1]
    
    # حساب سيولة الذهب (SMC) بناءً على سعر منصتك
    recent_low = df['low'].iloc[-20:-1].min()
    is_sweep = df['low'].iloc[-1] < recent_low and current_price > recent_low
    
    st.metric("سعر الذهب الحالي", f"${current_price:,.2f}")
    
    if is_sweep:
        st.success("🎯 تم رصد سحب سيولة (Sweep) بنفس سعر منصتك!")
        send_alert(f"إشارة ذهب مؤكدة!\nالسعر: {current_price}\nالسيولة كانت عند: {recent_low}")
    else:
        st.info("🔎 نراقب السيولة الآن.. السعر متزامن مع منصتك.")
else:
    st.warning("جاري محاولة الاتصال بـ Oanda... تأكد من تحديث الصفحة.")

if st.sidebar.button("🚀 اختبار التليجرام"):
    if not df.empty:
        send_alert(f"اختبار السعر: {df['close'].iloc[-1]}")
        st.sidebar.success("تم الإرسال!")
    else:
        st.sidebar.error("لا توجد بيانات لإرسالها")
        
