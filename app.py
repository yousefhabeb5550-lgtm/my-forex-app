import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 1. إعدادات الزوج والبيانات
pair = "EURUSD=X" 
data = yf.download(pair, period="5d", interval="15m")

# 2. خوارزمية اكتشاف الهيكل (BOS) ومناطق SMC
def get_smc_analysis(df):
    df = df.copy()
    # تحديد القمم والقيعان المحلية
    df['Peak'] = (df['High'] > df['High'].shift(1)) & (df['High'] > df['High'].shift(-1))
    df['Trough'] = (df['Low'] < df['Low'].shift(1)) & (df['Low'] < df['Low'].shift(-1))
    
    # تحديد مناطق العرض والطلب (أعلى قمة وأدنى قاع في الفترة الأخيرة)
    top_zone = df['High'].rolling(window=20).max().iloc[-1]
    bottom_zone = df['Low'].rolling(window=20).min().iloc[-1]
    
    return df, top_zone, bottom_zone

df, top_z, bottom_z = get_smc_analysis(data)
current_price = df['Close'].iloc[-1]

# 3. بناء الرسم البياني الاحترافي
fig = go.Figure()

# رسم الشموع اليابانية بألوان عالية التباين
fig.add_trace(go.Candlestick(
    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
    increasing_line_color='#00ffcc', decreasing_line_color='#ff3366',
    name="حركة السعر"
))

# إضافة منطقة البيع (Supply/Order Block) - بالأحمر
fig.add_hrect(y0=top_z - 0.0007, y1=top_z, fillcolor="#ff3366", opacity=0.3, line_width=0)
fig.add_annotation(x=df.index[-5], y=top_z, text="📉 منطقة بيع (SMC)", showarrow=False, 
                   font=dict(size=20, color="#ff3366"), bgcolor="black")

# إضافة منطقة الشراء (Demand/Order Block) - بالأخضر
fig.add_hrect(y0=bottom_z, y1=bottom_z + 0.0007, fillcolor="#00ffcc", opacity=0.3, line_width=0)
fig.add_annotation(x=df.index[-5], y=bottom_z, text="📈 منطقة شراء (SMC)", showarrow=False, 
                   font=dict(size=20, color="#00ffcc"), bgcolor="black")

# تحديد ورسم كسر الهيكل (BOS) - خطوط أفقية متقطعة
last_peak = df[df['Peak']]['High'].iloc[-2] if len(df[df['Peak']]) > 1 else top_z
if current_price > last_peak:
    fig.add_hline(y=last_peak, line_dash="dash", line_color="white", line_width=2)
    fig.add_annotation(x=df.index[10], y=last_peak, text="BOS (كسر هيكل صاعد)", font=dict(color="white", size=14))

# 4. تحسينات الواجهة والخطوط (UI/UX)
fig.update_layout(
    title=dict(
        text=f"📊 تحليل SMC لـ {pair} | السعر: {current_price:.5f}",
        font=dict(size=28, color="#00ffcc")
    ),
    template="plotly_dark",
    height=800,
    yaxis=dict(
        tickfont=dict(size=18, color="yellow"),
        gridcolor="#222222",
        side="right" # وضع السعر على اليمين كما في منصات التداول
    ),
    xaxis=dict(tickfont=dict(size=16), gridcolor="#222222"),
    paper_bgcolor="#0a0a0a",
    plot_bgcolor="#0a0a0a",
    margin=dict(l=20, r=20, t=60, b=20)
)

fig.show()
