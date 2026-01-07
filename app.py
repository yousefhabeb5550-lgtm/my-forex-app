import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import pytz
import requests

# --- إعدادات التليجرام ---
TOKEN = "8514661948:AAEBpNWf112SXZ5t5GoOCOR8-iLcwYENil4"
CHAT_ID = "8541033784"

def send_gold_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        full_msg = f"🪙 **[قناص الذهب SMC]**\n{message}"
        requests.post(url, data={"chat_id": CHAT_ID, "text": full_msg, "parse_mode": "Markdown"})
    except: pass

# --- إعدادات الذهب (XAU/USD) ---
GOLD_SYMBOL = "XAUUSD=X" 
SL_POINTS = 0.50  # 50 نقطة (أمان الذهب)
TP_POINTS = 1.50  # 150 نقطة (هدف 1:3)

st.set_page_config(page_title="Gold Sniper SMC", page_icon="🪙", layout="wide")

# --- جلب ومعالجة البيانات ---
def get_data():
    try:
        # جلب بيانات دقيقة واحدة لدقة الـ FVG والـ Sweep
        df = yf.Ticker(GOLD_SYMBOL).history(period="1d", interval="1m")
        return df
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    # حساب المؤشرات الفنية
    price = round(df['Close'].iloc[-1], 2)
    prev_close = df['Close'].iloc[-2]
    
    # 1. رصد سحب السيولة (Liquidity Sweep) - درس الفيديو 1
    recent_low = df['Low'].iloc[-20:-1].min()
    is_sweep = df['Low'].iloc[-1] < recent_low and price > recent_low
    
    # 2. رصد الفجوة السعرية (FVG) - درس الفيديو 2
    # نتحقق من وجود فجوة بين شمعة اليوم وشمعة ما قبل الانفجار
    has_fvg = df['Low'].iloc[-1] > df['High'].iloc[-3]
    
    # 3. فلتر الوقت (توقيت نيويورك) - درس الفيديو 3
    tz = pytz.timezone('Africa/Tripoli')
    now_hour = datetime.now(tz).hour
    is_silver_bullet = (15 <= now_hour <= 16) # من 3 لـ 4 عصراً

    # --- منطق الإشارة الذكية ---
    if is_sweep and has_fvg:
        entry = price
        sl = entry - SL_POINTS
        tp = entry + TP_POINTS
        
        msg = (f"🚀 **فرصة قنص ذهب مؤكدة**\n\n"
               f"💰 سعر الدخول: {entry}\n"
               f"🛑 الستوب: {sl}\n"
               f"✅ الهدف: {tp}\n\n"
               f"📊 الفلتر: سحب سيولة + FVG اكتملت\n"
               f"⏰ التوقيت: {'Silver Bullet نشط 🔥' if is_silver_bullet else 'خارج الذروة'}")
        
        # منع التكرار
        if 'last_gold_trade' not in st.session_state or st.session_state.last_gold_trade != price:
            send_gold_alert(msg)
            st.session_state.last_gold_trade = price

    # --- واجهة المنصة الاحترافية ---
    st.title("🪙 رادار الذهب - استراتيجية الأموال الذكية (SMC)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("السعر الحالي (XAU/USD)", f"${price}")
    col2.metric("حالة السيولة", "سحب سيولة ✅" if is_sweep else "انتظار كسر")
    col3.metric("توقيت نيويورك", "نشط ⚡️" if is_silver_bullet else "خامل")

    st.markdown("---")
    
    # عرض حالة الفجوة السعرية
    if has_fvg:
        st.success("✅ تم اكتشاف فجوة سعرية (FVG) - الزخم الشرائي قوي جداً!")
    else:
        st.info("🕒 بانتظار تكون فجوة سعرية (FVG) لتأكيد الدخول المؤسساتي...")

    # القائمة الجانبية
    st.sidebar.header("🛠️ تحكم القناص")
    if st.sidebar.button("🚀 اختبار اتصال التليجرام"):
        send_gold_alert(f"فحص الاتصال ناجح! السعر الحالي في الرادار: {price}")
        st.sidebar.success("تم الإرسال!")

    st.sidebar.markdown("---")
    st.sidebar.write(f"📍 أدنى سيولة مرصودة: {recent_low}")
    
